from qdrant_client import QdrantClient

from app.services.embeddings_service import embed_chunks


from app.config.settings import settings


client = QdrantClient(
    host= settings.qdrant_host,
    port= settings.qdrant_port
)

async def retrieve_chunks(query: str,limit: int = 3):

    query_embedding = embed_chunks([query])[0]

    results = client.query_points(
        collection_name= settings.qdrant_collection_name,
        query=query_embedding,
        limit=limit
    )

    return [
        {
            "score": result.score,
            "text": result.payload["text"],
            "source": result.payload.get("source"),
            "chunk_id": result.payload.get("chunk_id")
        }
        for result in results.points
    ]