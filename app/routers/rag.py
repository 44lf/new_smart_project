from fastapi import APIRouter

from app.schemas.rag import RagQuery, RagResponse
from app.services.rag import RagService

router = APIRouter(prefix="/api/rag", tags=["rag"])


@router.post("/query_score", response_model=RagResponse)
async def query_score(payload: RagQuery) -> RagResponse:
    service = RagService()
    result = await service.query_score(payload.user_query, payload.top_k, payload.filters)
    return RagResponse(**result)
