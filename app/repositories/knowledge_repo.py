from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.knowledge_file import KnowledgeFile


class KnowledgeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, knowledge: KnowledgeFile) -> KnowledgeFile:
        self.session.add(knowledge)
        await self.session.commit()
        await self.session.refresh(knowledge)
        return knowledge

    async def list_paginated(self, offset: int, limit: int) -> list[KnowledgeFile]:
        result = await self.session.execute(
            select(KnowledgeFile).order_by(KnowledgeFile.created_at.desc()).offset(offset).limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_id(self, file_id: str) -> KnowledgeFile | None:
        result = await self.session.execute(select(KnowledgeFile).where(KnowledgeFile.file_id == file_id))
        return result.scalars().first()
