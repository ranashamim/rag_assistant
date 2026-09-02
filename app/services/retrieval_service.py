
from app.services.embeddings_service import embed_query

from app.config.settings import settings

from app.services.qdrant_service import client
from app.services.reranker_service import rerank


async def retrieve_chunks(query: str, candidate_limit: int = 10):

    query_embedding = embed_query(query)

    results = client.query_points(
        collection_name= settings.qdrant_collection_name,
        query=query_embedding,
        limit=candidate_limit
    )
    

    return [
            {
                "score": result.score,
                "text": result.payload["text"],
                "source": result.payload.get("source"),
                "chunk_id": result.payload.get("chunk_id"),
                "method": result.payload.get("method")
            }
            for result in results.points
        ]


async def rerank_retrieved_chunks(query: str, candidate_limit: int=10, rerank_limit: int=3):

    chunks = await retrieve_chunks(query, candidate_limit)

    reranked_chunks = rerank(query, chunks)

    return reranked_chunks[:rerank_limit]
