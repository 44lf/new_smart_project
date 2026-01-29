import re
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import AppError
from app.integrations.dify_client import DifyClient
from app.integrations.redis_client import get_redis


class Text2SQLService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.client = DifyClient()

    async def train(self, schema: str, examples: list[dict[str, Any]]) -> None:
        redis = get_redis()
        await redis.set("text2sql:schema", schema)
        await redis.set("text2sql:examples", str(examples))

    async def query(self, question: str) -> dict[str, Any]:
        payload = {
            "inputs": {"query": question},
            "response_mode": "blocking",
            "user": "text2sql",
        }
        result = await self.client.chat_messages(payload)
        sql = result.get("answer", "")
        sql = sql.strip()
        if not self._is_safe(sql):
            raise AppError(400, "Only SELECT statements are allowed")
        try:
            rows = await self.session.execute(text(sql))
            columns = list(rows.keys())
            data = [list(row) for row in rows.fetchall()]
            return {"sql": sql, "columns": columns, "rows": data}
        except Exception as exc:  # noqa: BLE001
            repaired_sql = await self._repair_sql(sql, str(exc))
            rows = await self.session.execute(text(repaired_sql))
            columns = list(rows.keys())
            data = [list(row) for row in rows.fetchall()]
            return {"sql": repaired_sql, "columns": columns, "rows": data, "error": str(exc)}

    def _is_safe(self, sql: str) -> bool:
        if settings.allow_write_sql:
            return True
        return bool(re.match(r"^\s*select\b", sql, re.IGNORECASE))

    async def _repair_sql(self, sql: str, error: str) -> str:
        prompt = {
            "inputs": {"query": f"SQL: {sql}\nError: {error}\nPlease output a fixed SELECT SQL only."},
            "response_mode": "blocking",
            "user": "text2sql",
        }
        result = await self.client.chat_messages(prompt)
        repaired = result.get("answer", sql)
        if not self._is_safe(repaired):
            raise AppError(400, "Repaired SQL is not safe")
        return repaired
