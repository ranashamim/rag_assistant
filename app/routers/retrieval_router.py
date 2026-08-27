from fastapi import APIRouter
from app.services.retrieval_service import retrieve_chunks

router = APIRouter(prefix="/retrieval", tags=["Query"])


@router.get("/get_query/{query}")
async def retrieve_docs(query: str):
    result = await retrieve_chunks(query)
    return result

