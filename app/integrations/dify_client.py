from typing import Any

import httpx

from app.core.config import settings


def _headers() -> dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if settings.dify_api_key:
        headers["Authorization"] = f"Bearer {settings.dify_api_key}"
    return headers


class DifyClient:
    def __init__(self) -> None:
        self.base_url = settings.dify_base_url.rstrip("/")
        self.headers = _headers()

    async def chat_messages(self, payload: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.base_url}/v1/chat-messages"
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()

    async def run_workflow(self, payload: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.base_url}/v1/workflows/run"
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
