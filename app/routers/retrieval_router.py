from fastapi import APIRouter
from app.services.conversation_service import get_conversation
from app.services.file_service import read_chunks_file
from app.services.generation_service import answer_query
from app.services.parent_child_service import deduplicate_parents, expand_results, expand_to_parent, group_by_parent
from app.services.retrieval_service import hybrid_retrieve
from app.services.retriever import BM25Retriever, DenseRetriever
from app.services.router_service import adaptive_retrieve, build_parent_child_context

router = APIRouter(prefix="/retrieval", tags=["Query"])


@router.get("/get_query/{conversation_id}/{query}")
async def retrieve_docs(conversation_id: str, query: str):
    result = await answer_query(query, conversation_id)
    return result


@router.get("/test/{query}")
async def evaulate(query: str):

    r = get_conversation(query)

    
    return r

    

    
