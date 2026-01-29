from pydantic import BaseModel


class KnowledgeFileOut(BaseModel):
    file_id: str
    file_name: str
    object_key: str
    file_type: str
    file_size: int
    upload_time: str
    uploader: str


class KnowledgeUploadResult(BaseModel):
    file_id: str
    chunks: int
    failed_chunks: int
    elapsed_ms: int
