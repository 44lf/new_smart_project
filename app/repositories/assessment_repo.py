from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.assessment import UserHealthRiskAssessment


class AssessmentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, assessment: UserHealthRiskAssessment) -> UserHealthRiskAssessment:
        self.session.add(assessment)
        await self.session.commit()
        await self.session.refresh(assessment)
        return assessment

    async def latest_by_user(self, user_id: int) -> UserHealthRiskAssessment | None:
        result = await self.session.execute(
            select(UserHealthRiskAssessment)
            .where(UserHealthRiskAssessment.user_id == user_id)
            .order_by(UserHealthRiskAssessment.created_at.desc())
        )
        return result.scalars().first()
