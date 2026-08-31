from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from app.config.settings import settings


client = QdrantClient(
    host=settings.qdrant_host,
    port=settings.qdrant_port,
)

def get_distance():
    if settings.embedding_distance.lower() == "cosine":
        return Distance.COSINE

    raise ValueError(
        f"Unsupported distance: {settings.embedding_distance}"
    )

def create_collection():
    collections = client.get_collections().collections

    collection_names = [collection.name for collection in collections]

    if settings.qdrant_collection_name not in collection_names:
        client.create_collection(
            collection_name=settings.qdrant_collection_name,
            vectors_config=VectorParams(
                size=settings.embedding_dimension,
                distance=get_distance(),
            ),
        )

        print(
            f"Collection '{settings.qdrant_collection_name}' created."
        )