from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.repositories.knowledge_repo import KnowledgeRepository
from app.schemas.knowledge import KnowledgeFileOut, KnowledgeUploadResult
from app.services.knowledge import KnowledgeService

router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])


@router.post("/upload", response_model=KnowledgeUploadResult)
async def upload_knowledge(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_db),
) -> KnowledgeUploadResult:
    content = await file.read()
    service = KnowledgeService(KnowledgeRepository(session))
    result = await service.upload_file(file.filename, content, uploader="system")
    return KnowledgeUploadResult(**result)


@router.get("/files", response_model=list[KnowledgeFileOut])
async def list_files(
    page: int = 1,
    size: int = 10,
    session: AsyncSession = Depends(get_db),
) -> list[KnowledgeFileOut]:
    repo = KnowledgeRepository(session)
    offset = (page - 1) * size
    items = await repo.list_paginated(offset, size)
    return [KnowledgeFileOut(**item.__dict__) for item in items]
