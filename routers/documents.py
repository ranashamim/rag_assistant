from fastapi import APIRouter, Depends, File, UploadFile
from services.file_service import extract_text, read_chunks_file, save_chunks_to_file
from services.chunking_service import chunk_document

router = APIRouter(prefix="/docs", tags=["Document"])


@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    result = await extract_text(file)

    chunks = chunk_document(
        text=result,
        source=file.filename,
        method="punctuation"
    )

    print(await save_chunks_to_file(chunks))

    return {
            "message": "File processed successfully",
            "text_length": len(result),
            "chunks": chunks
        }


@router.get("/chunks/")
async def get_chunks():
    chunks = await read_chunks_file()
    return {
            "count": len(chunks),
            "chunks": chunks
        }