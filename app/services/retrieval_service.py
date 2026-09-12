from app.services.fusion_service import reciprocal_rank_fusion
from app.services.reranker_service import rerank

from app.services.retriever import BM25Retriever, DenseRetriever, HybridRetriever


async def rerank_retrieved_chunks(query: str, candidate_limit: int=10, rerank_limit: int=3):
    
    dense = DenseRetriever()
    chunks = await dense.retrieve(query, candidate_limit)

    reranked_chunks = rerank(query, chunks)

    return reranked_chunks[:rerank_limit]



def rerank_chunks(query, chunks, rerank_limit=3):

    reranked_chunks = rerank(query, chunks)

    return reranked_chunks[:rerank_limit]



async def hybrid_retrieve(query, candidate_limit=10):

    hybrid = HybridRetriever()
    fused_results = await hybrid.retrieve(query, candidate_limit)
    reranked_chunks = rerank_chunks(query, fused_results)

    return reranked_chunks


