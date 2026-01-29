from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.schemas.text2sql import Text2SQLQueryRequest, Text2SQLResponse, Text2SQLTrainRequest
from app.services.text2sql import Text2SQLService

router = APIRouter(prefix="/api/text2sql", tags=["text2sql"])


@router.post("/train")
async def train(payload: Text2SQLTrainRequest, session: AsyncSession = Depends(get_db)) -> dict:
    service = Text2SQLService(session)
    await service.train(payload.schema, payload.examples)
    return {"status": "ok"}


@router.post("/query", response_model=Text2SQLResponse)
async def query(payload: Text2SQLQueryRequest, session: AsyncSession = Depends(get_db)) -> Text2SQLResponse:
    service = Text2SQLService(session)
    result = await service.query(payload.query)
    return Text2SQLResponse(**result)
