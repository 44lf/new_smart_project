from typing import Any

from app.schemas.mcp import Heartbeat, ServiceRegistration


class MCPRegistry:
    def __init__(self) -> None:
        self.services: dict[str, dict[str, Any]] = {}

    def register(self, payload: ServiceRegistration) -> None:
        self.services[payload.name] = {"url": payload.url, "metadata": payload.metadata}

    def heartbeat(self, payload: Heartbeat) -> dict[str, Any]:
        return {"service": payload.service_name, "status": payload.status}

    def list_services(self) -> dict[str, dict[str, Any]]:
        return self.services
