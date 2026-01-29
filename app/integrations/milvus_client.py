from pymilvus import Collection, CollectionSchema, DataType, FieldSchema, connections, utility

from app.core.config import settings


def connect_milvus() -> None:
    connections.connect(host=settings.milvus_host, port=settings.milvus_port)


def ensure_collection() -> Collection:
    connect_milvus()
    if utility.has_collection(settings.milvus_collection):
        return Collection(settings.milvus_collection)

    fields = [
        FieldSchema(name="chunk_id", dtype=DataType.VARCHAR, is_primary=True, max_length=64),
        FieldSchema(name="file_id", dtype=DataType.VARCHAR, max_length=64),
        FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
        FieldSchema(name="metadata", dtype=DataType.JSON),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=768),
    ]
    schema = CollectionSchema(fields, description="knowledge chunks")
    collection = Collection(settings.milvus_collection, schema=schema)
    return collection


def ensure_index(collection: Collection) -> None:
    if collection.has_index():
        return
    index_params = {"metric_type": "IP", "index_type": "IVF_FLAT", "params": {"nlist": 128}}
    collection.create_index("embedding", index_params)
