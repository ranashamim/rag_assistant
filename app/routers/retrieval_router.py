from fastapi import APIRouter
from app.services.query_transformation_service import generate_multi_queries
from app.services.router_service import adaptive_retrieve
from app.test.evaluation_chunking_strategies import evaluation

router = APIRouter(prefix="/retrieval", tags=["Query"])


@router.get("/get_query/{query}")
async def retrieve_docs(query: str):
    result = await adaptive_retrieve(query)
    return result

@router.get("/evaluation/")
async def evaulate():
    result = await evaluation()
    return result


@router.get("/test/{query}")
async def evaulate(query: str):
    results = generate_multi_queries(query)
    return results

    
