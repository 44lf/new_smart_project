from pydantic import BaseModel


class ServiceRegistration(BaseModel):
    name: str
    url: str
    metadata: dict | None = None


class Heartbeat(BaseModel):
    service_name: str
    status: str
