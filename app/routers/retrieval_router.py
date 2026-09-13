from fastapi import APIRouter
from app.services.file_service import read_chunks_file
from app.services.generation_service import answer_query
from app.services.retrieval_service import hybrid_retrieve
from app.services.retriever import BM25Retriever, DenseRetriever, expand_to_parent
from app.services.router_service import adaptive_retrieve

router = APIRouter(prefix="/retrieval", tags=["Query"])


@router.get("/get_query/{query}")
async def retrieve_docs(query: str):
    result = await answer_query(query)
    return result



@router.get("/test/{query}")
async def evaulate(query: str):

    dense = DenseRetriever()

    result = await dense.retrieve(query, 5)
    resultt = result[0]

    print("Child:", resultt.child.text)
    print("Parent:", resultt.parent.text)
    print("Score:", resultt.score)

    return resultt

    

    
