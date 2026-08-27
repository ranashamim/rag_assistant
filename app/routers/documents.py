from fastapi import APIRouter, File, UploadFile
from app.services.file_service import extract_text, read_chunks_file, save_chunks_to_file
from app.services.retrieval_service import retrieve_chunks
from app.services.vector_service import to_db_vector

router = APIRouter(prefix="/docs", tags=["Document"])


@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    vector = await to_db_vector(file, "punctuation")
    return vector


@router.get("/chunks/")
async def get_chunks():
    chunks = read_chunks_file()
    return {
            "count": len(chunks),
            "chunks": chunks
        }


