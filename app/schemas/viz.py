from pydantic import BaseModel


class EChartsRequest(BaseModel):
    columns: list[str]
    rows: list[list]


class EChartsResponse(BaseModel):
    echarts_option: dict
