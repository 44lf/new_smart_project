from pydantic import BaseModel


class ScoreResult(BaseModel):
    total_score: int
    nutritional_impairment_score: int
    disease_severity_score: int
    age_score: int
    risk_level: str
    recommendations: str
    assessment_basis: str


class SourceBasis(BaseModel):
    chunk_id: str
    file_id: str
    snippet: str
    score: float
    reason: str
