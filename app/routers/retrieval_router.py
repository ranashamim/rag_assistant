from fastapi import APIRouter
from app.services.generation_service import answer_query
from app.services.retrieval_service import hybrid_retrieve
from app.services.retriever import BM25Retriever, DenseRetriever
from app.services.router_service import adaptive_retrieve

router = APIRouter(prefix="/retrieval", tags=["Query"])


@router.get("/get_query/{query}")
async def retrieve_docs(query: str):
    result = await answer_query(query)
    return result


@router.get("/test/{query}")
async def evaulate(query: str):
    
    result = await hybrid_retrieve(query, 5)
    return result

    

    
