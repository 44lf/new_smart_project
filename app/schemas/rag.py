from pydantic import BaseModel, Field

from app.schemas.assessment import ScoreResult, SourceBasis


class RagQuery(BaseModel):
    user_query: str
    top_k: int = Field(default=5, ge=1, le=20)
    filters: dict | None = None


class RagResponse(BaseModel):
    user_query: str
    score_result: ScoreResult
    source_basis: list[SourceBasis]
