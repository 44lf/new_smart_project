from fastapi import APIRouter, Depends
from sqlalchemy import text

from app.core.deps import get_db
from app.integrations.minio_client import get_minio_client
from app.integrations.milvus_client import connect_milvus
from app.integrations.redis_client import get_redis
from app.schemas.mcp import Heartbeat, ServiceRegistration
from app.services.mcp import MCPRegistry

router = APIRouter(tags=["mcp"])
registry = MCPRegistry()


@router.get("/health")
async def health(session=Depends(get_db)) -> dict:
    mysql_status = "ok"
    redis_status = "ok"
    milvus_status = "ok"
    minio_status = "ok"
    try:
        await session.execute(text("SELECT 1"))
    except Exception as exc:  # noqa: BLE001
        mysql_status = str(exc)
    try:
        redis = get_redis()
        await redis.ping()
    except Exception as exc:  # noqa: BLE001
        redis_status = str(exc)
    try:
        connect_milvus()
    except Exception as exc:  # noqa: BLE001
        milvus_status = str(exc)
    try:
        minio = get_minio_client()
        minio.list_buckets()
    except Exception as exc:  # noqa: BLE001
        minio_status = str(exc)
    return {
        "mysql": mysql_status,
        "redis": redis_status,
        "milvus": milvus_status,
        "minio": minio_status,
    }


@router.post("/mcp/heartbeat")
async def heartbeat(payload: Heartbeat) -> dict:
    return registry.heartbeat(payload)


@router.post("/mcp/services/register")
async def register_service(payload: ServiceRegistration) -> dict:
    registry.register(payload)
    return {"status": "registered"}


@router.get("/mcp/services")
async def list_services() -> dict:
    return registry.list_services()
