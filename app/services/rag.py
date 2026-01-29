import json
from typing import Any

from rank_bm25 import BM25Okapi

from app.core.config import settings
from app.core.exceptions import AppError
from app.integrations.milvus_client import ensure_collection, ensure_index
from app.integrations.ollama_client import get_embeddings, get_llm
from app.schemas.assessment import ScoreResult, SourceBasis
from app.services.cache import cacheable


class RagService:
    def __init__(self) -> None:
        self.collection = ensure_collection()
        ensure_index(self.collection)
        self.embeddings = get_embeddings()
        self.llm = get_llm()

    @cacheable(ttl=settings.cache_ttl_seconds, namespace=settings.cache_namespace)
    async def query_score(self, user_query: str, top_k: int, filters: dict | None) -> dict[str, Any]:
        retrieved = self._retrieve(user_query, top_k, filters)
        score_result = await self._generate_score(user_query, retrieved)
        return {
            "user_query": user_query,
            "score_result": score_result.model_dump(),
            "source_basis": [item.model_dump() for item in retrieved],
        }

    def _retrieve(self, user_query: str, top_k: int, filters: dict | None) -> list[SourceBasis]:
        vector = self.embeddings.embed_query(user_query)
        self.collection.load()
        expr = None
        if filters and "file_id" in filters:
            expr = f"file_id == '{filters['file_id']}'"
        results = self.collection.search(
            data=[vector],
            anns_field="embedding",
            param={"metric_type": "IP", "params": {"nprobe": 10}},
            limit=top_k * 3,
            expr=expr,
            output_fields=["file_id", "text", "metadata"],
        )
        hits = results[0]
        docs = [hit.entity.get("text") for hit in hits]
        tokenized = [doc.split() for doc in docs]
        bm25 = BM25Okapi(tokenized) if docs else None
        scores = bm25.get_scores(user_query.split()) if bm25 else []
        max_score = max(scores) if scores else 1
        min_score = min(scores) if scores else 0
        sources: list[SourceBasis] = []
        for idx, hit in enumerate(hits):
            bm25_score = scores[idx] if scores else 0
            normalized = (bm25_score - min_score) / (max_score - min_score + 1e-6)
            final_score = settings.rag_bm25_weight * normalized + settings.rag_vector_weight * hit.score
            sources.append(
                SourceBasis(
                    chunk_id=hit.id,
                    file_id=hit.entity.get("file_id"),
                    snippet=hit.entity.get("text")[:200],
                    score=float(final_score),
                    reason="融合 BM25 + 向量召回",
                )
            )
        sources.sort(key=lambda item: item.score, reverse=True)
        return sources[:top_k]

    async def _generate_score(self, user_query: str, sources: list[SourceBasis]) -> ScoreResult:
        context = "\n".join([f"[{s.file_id}] {s.snippet}" for s in sources])
        prompt = (
            "你是营养风险评估专家，使用 NRS2002 评分标准。总分=营养受损(0-3)+疾病严重度(0-3)+年龄(0-1)。"
            "总分>=3为高风险。请基于用户问题和参考文本给出严格 JSON 输出，字段："
            "total_score,nutritional_impairment_score,disease_severity_score,age_score,risk_level,"
            "recommendations,assessment_basis。不要输出多余文本。\n"
            f"用户问题: {user_query}\n参考: {context}"
        )
        for attempt in range(2):
            response = await self.llm.ainvoke(prompt)
            try:
                data = json.loads(response.content)
                return ScoreResult(**data)
            except json.JSONDecodeError as exc:
                if attempt == 1:
                    raise AppError(500, f"LLM 输出不是合法 JSON: {exc}") from exc
        raise AppError(500, "评分失败")
