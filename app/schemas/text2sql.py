from pydantic import BaseModel


class Text2SQLTrainRequest(BaseModel):
    schema: str
    examples: list[dict]


class Text2SQLQueryRequest(BaseModel):
    query: str


class Text2SQLResponse(BaseModel):
    sql: str
    columns: list[str]
    rows: list[list]
    chart_suggestion: dict | None = None
    error: str | None = None
