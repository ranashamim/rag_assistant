
from app.services.embeddings_service import embed_query

from app.config.settings import settings

from app.services.fusion_service import reciprocal_rank_fusion
from app.services.qdrant_service import client
from app.services.reranker_service import rerank

from app.services.file_service import read_chunks_file

from app.services.bm25_service import build_bm25_index, search_bm25


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



chunks = read_chunks_file()
bm25_index = build_bm25_index(chunks)

def get_bm25_results(query, limit=10):
    
    related_chunks = search_bm25(bm25= bm25_index, query=query, chunks=chunks, limit=limit)

    return related_chunks


def rerank_chunks(query, chunks, rerank_limit=3):

    reranked_chunks = rerank(query, chunks)

    return reranked_chunks[:rerank_limit]



async def hybrid_retrieve(query, candidate_limit=10):
    semantic_results = await retrieve_chunks(query, candidate_limit)
    bm25_results = get_bm25_results(query, candidate_limit)
    fused_results = reciprocal_rank_fusion([semantic_results, bm25_results])
    reranked_chunks = rerank_chunks(query, fused_results)

    return reranked_chunks


