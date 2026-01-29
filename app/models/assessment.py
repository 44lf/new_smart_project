from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class UserHealthRiskAssessment(Base):
    __tablename__ = "user_health_risk_assessment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_name: Mapped[str] = mapped_column(String(128), nullable=False)
    sex: Mapped[str] = mapped_column(String(16), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    assessment_time: Mapped[str] = mapped_column(String(64), nullable=False)
    assessment_count: Mapped[int] = mapped_column(Integer, default=1)
    total_score: Mapped[int] = mapped_column(Integer, nullable=False)
    nutritional_impairment_score: Mapped[int] = mapped_column(Integer, nullable=False)
    disease_severity_score: Mapped[int] = mapped_column(Integer, nullable=False)
    age_score: Mapped[int] = mapped_column(Integer, nullable=False)
    assessment_basis: Mapped[str] = mapped_column(Text, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(32), nullable=False)
    recommendations: Mapped[str] = mapped_column(Text, nullable=False)
    bmi: Mapped[str | None] = mapped_column(String(32))
    weight_change: Mapped[str | None] = mapped_column(String(64))
    disease_condition: Mapped[str | None] = mapped_column(String(255))
    dietary_intake: Mapped[str | None] = mapped_column(String(255))
