from fastapi import APIRouter

from app.schemas.viz import EChartsRequest, EChartsResponse
from app.services.echarts import generate_echarts_option

router = APIRouter(prefix="/api/viz", tags=["viz"])


@router.post("/echarts", response_model=EChartsResponse)
async def echarts(payload: EChartsRequest) -> EChartsResponse:
    option = generate_echarts_option(payload.columns, payload.rows)
    return EChartsResponse(echarts_option=option)
