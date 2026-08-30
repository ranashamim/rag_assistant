from fastapi import APIRouter, File, UploadFile
from app.services.chunking_service import chunk_document
from app.services.file_service import parse_document, read_chunks_file
from app.services.semantic_chunking_service import semantic_chunk
from app.services.vector_service import to_db_vector

router = APIRouter(prefix="/docs", tags=["Document"])


@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    vector = await to_db_vector(file, "semantic")
    return vector


@router.get("/chunks/")
async def get_chunks():
    chunks = read_chunks_file()
    return {
            "count": len(chunks),
            "chunks": chunks
        }

text = """
FastAPI is a Python framework for building APIs.
It is based on standard Python type hints.

FastAPI supports asynchronous programming.
It also provides automatic API documentation.

Retrieval augmented generation combines retrieval
with language model generation.
"""

@router.get("/testchunks/")
async def get_chunk_test():
    chunks = semantic_chunk(
        text,
        percentile=25
    )
    return chunks


@router.post("/upload_test/")
async def upload_file(file: UploadFile = File(...)):
    text = await parse_document(file)
    
    chunks = chunk_document(
            text=text,
            source=file.filename,
            method="semantic"
        )

    return chunks


