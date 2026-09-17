from fastapi import APIRouter
from app.services.file_service import read_chunks_file
from app.services.generation_service import answer_query
from app.services.parent_child_service import deduplicate_parents, expand_results, expand_to_parent, group_by_parent
from app.services.retrieval_service import hybrid_retrieve
from app.services.retriever import BM25Retriever, DenseRetriever
from app.services.router_service import adaptive_retrieve, build_parent_child_context

router = APIRouter(prefix="/retrieval", tags=["Query"])


@router.get("/get_query/{query}")
async def retrieve_docs(query: str):
    result = await answer_query(query)
    return result



@router.get("/test/{query}")
async def evaulate(query: str):

    chunks = read_chunks_file()

    print("Total chunks in chunks.json:", len(chunks))

    for chunk in chunks:
        print(chunk.source, chunk.chunk_id)

    
    return None

    

    
