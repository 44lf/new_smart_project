from datetime import datetime

from app.models.assessment import UserHealthRiskAssessment
from app.repositories.assessment_repo import AssessmentRepository
from app.schemas.assessment import ScoreResult


class AssessmentService:
    def __init__(self, repo: AssessmentRepository) -> None:
        self.repo = repo

    async def save_assessment(
        self,
        user_id: int,
        user_name: str,
        sex: str,
        age: int,
        score: ScoreResult,
        bmi: str | None = None,
        weight_change: str | None = None,
        disease_condition: str | None = None,
        dietary_intake: str | None = None,
    ) -> UserHealthRiskAssessment:
        assessment = UserHealthRiskAssessment(
            user_id=user_id,
            user_name=user_name,
            sex=sex,
            age=age,
            assessment_time=datetime.utcnow().isoformat(),
            assessment_count=1,
            total_score=score.total_score,
            nutritional_impairment_score=score.nutritional_impairment_score,
            disease_severity_score=score.disease_severity_score,
            age_score=score.age_score,
            assessment_basis=score.assessment_basis,
            risk_level=score.risk_level,
            recommendations=score.recommendations,
            bmi=bmi,
            weight_change=weight_change,
            disease_condition=disease_condition,
            dietary_intake=dietary_intake,
        )
        return await self.repo.create(assessment)
