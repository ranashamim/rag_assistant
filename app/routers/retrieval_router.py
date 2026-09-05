from fastapi import APIRouter
from app.services.generation_service import answer_query, generate_answer
from app.services.retrieval_service import rerank_retrieved_chunks
from app.services.router_service import adaptive_retrieve, build_context, retrieve_decomposed, rewrite_query
from app.test.evaluation_chunking_strategies import evaluation

router = APIRouter(prefix="/retrieval", tags=["Query"])


@router.get("/get_query/{query}")
async def retrieve_docs(query: str):
    result = await rerank_retrieved_chunks(query)
    return result

@router.get("/evaluation/")
async def evaulate():
    result = await evaluation()
    return result


@router.get("/test/{query}")
async def evaulate(query: str):
    response = await answer_query(query=query)
    return response
