import io
import time
from datetime import datetime
from typing import Any

import pandas as pd
from pymilvus import Collection

from app.core.config import settings
from app.core.exceptions import AppError
from app.integrations.minio_client import get_minio_client
from app.integrations.milvus_client import ensure_collection, ensure_index
from app.integrations.ollama_client import get_embeddings
from app.models.knowledge_file import KnowledgeFile
from app.repositories.knowledge_repo import KnowledgeRepository

ALLOWED_TYPES = {".pdf", ".doc", ".docx", ".txt", ".md", ".xlsx", ".xls", ".csv"}


class KnowledgeService:
    def __init__(self, repo: KnowledgeRepository):
        self.repo = repo

    async def upload_file(self, filename: str, content: bytes, uploader: str) -> dict[str, Any]:
        ext = self._validate_extension(filename)
        start = time.time()
        file_id = await self._save_metadata(filename, content, ext, uploader)
        text = self._extract_text(filename, content, ext)
        chunks = self._split_text(text)
        collection = ensure_collection()
        ensure_index(collection)
        embeddings = get_embeddings()
        upserted = self._upsert_chunks(collection, file_id, filename, chunks, embeddings)
        elapsed_ms = int((time.time() - start) * 1000)
        return {"file_id": file_id, "chunks": upserted, "failed_chunks": len(chunks) - upserted, "elapsed_ms": elapsed_ms}

    async def _save_metadata(self, filename: str, content: bytes, ext: str, uploader: str) -> str:
        minio = get_minio_client()
        object_key = f"{datetime.utcnow().strftime('%Y%m%d')}/{filename}"
        bucket = settings.minio_bucket
        if not minio.bucket_exists(bucket):
            minio.make_bucket(bucket)
        minio.put_object(bucket, object_key, io.BytesIO(content), length=len(content))
        knowledge = KnowledgeFile(
            file_name=filename,
            object_key=object_key,
            file_type=ext,
            file_size=len(content),
            upload_time=datetime.utcnow().isoformat(),
            uploader=uploader,
        )
        saved = await self.repo.create(knowledge)
        return saved.file_id

    def _validate_extension(self, filename: str) -> str:
        ext = "." + filename.split(".")[-1].lower()
        if ext not in ALLOWED_TYPES:
            raise AppError(400, f"Unsupported file type: {ext}")
        return ext

    def _extract_text(self, filename: str, content: bytes, ext: str) -> str:
        if ext in {".txt", ".md"}:
            return content.decode("utf-8", errors="ignore")
        if ext == ".csv":
            df = pd.read_csv(io.BytesIO(content))
            return df.to_csv(index=False)
        if ext in {".xlsx", ".xls"}:
            df = pd.read_excel(io.BytesIO(content))
            return df.to_csv(index=False)
        if ext == ".pdf":
            import pdfplumber

            text_parts = []
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                for page in pdf.pages:
                    text_parts.append(page.extract_text() or "")
            return "\n".join(text_parts)
        if ext in {".doc", ".docx"}:
            import docx

            doc = docx.Document(io.BytesIO(content))
            return "\n".join([p.text for p in doc.paragraphs])
        raise AppError(400, f"No parser for file type: {ext}")

    def _split_text(self, text: str) -> list[str]:
        parts = [p.strip() for p in text.split("\n\n") if p.strip()]
        chunks: list[str] = []
        for part in parts:
            if len(part) <= 500:
                chunks.append(part)
            else:
                for i in range(0, len(part), 500):
                    chunks.append(part[i : i + 500])
        return chunks

    def _upsert_chunks(
        self, collection: Collection, file_id: str, filename: str, chunks: list[str], embeddings
    ) -> int:
        vectors = embeddings.embed_documents(chunks)
        payload = [
            [f"{file_id}-{idx}" for idx in range(len(chunks))],
            [file_id] * len(chunks),
            chunks,
            [{"file_name": filename, "chunk_index": idx} for idx in range(len(chunks))],
            vectors,
        ]
        if not chunks:
            return 0
        collection.insert(payload)
        return len(chunks)
