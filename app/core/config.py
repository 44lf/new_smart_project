from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_host: str = "0.0.0.0"
    app_port: int = 8018
    log_level: str = "INFO"

    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_db: str = "nutrition"
    mysql_user: str = "nutrition"
    mysql_password: str = "nutrition"
    mysql_uri: str = "mysql+aiomysql://nutrition:nutrition@localhost:3306/nutrition"

    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str | None = None

    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_bucket: str = "kb"

    milvus_host: str = "localhost"
    milvus_port: int = 19530
    milvus_collection: str = "knowledge_chunks"

    ollama_base_url: str = "http://localhost:11434"
    ollama_llm_model: str = "llama3.1"
    ollama_embed_model: str = "nomic-embed-text"
    ollama_rerank_model: str | None = None

    dify_base_url: str = "http://localhost:5001"
    dify_api_key: str | None = None
    dify_app_id: str | None = None

    jwt_secret: str = "change_me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    cache_ttl_seconds: int = 600
    cache_namespace: str = "rag"
    rag_bm25_weight: float = 0.4
    rag_vector_weight: float = 0.6
    rag_top_k: int = 5

    allow_write_sql: bool = False


settings = Settings()
