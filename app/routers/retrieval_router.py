from fastapi import APIRouter
from app.services.generation_service import answer_query
from app.services.query_transformation_service import retrieve_multi_query
from app.services.retrieval_service import get_bm25_results, hybrid_retrieve
from app.services.retriever import BM25Retriever, DenseRetriever
from app.services.router_service import adaptive_retrieve
from app.test.evaluation_chunking_strategies import evaluation

router = APIRouter(prefix="/retrieval", tags=["Query"])


@router.get("/get_query/{query}")
async def retrieve_docs(query: str):
    result = await answer_query(query)
    return result

@router.get("/evaluation/")
async def evaulate():
    result = await evaluation()
    return result


@router.get("/test/{query}")
async def evaulate(query: str):
    dense = DenseRetriever()
    bm25 = BM25Retriever()
    await dense.retrieve("What is RAG?", 5)
    await bm25.retrieve("What is RAG?", 5)
    # results = await hybrid_retrieve(query)
    # return results

    
