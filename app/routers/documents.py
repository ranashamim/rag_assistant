from fastapi import APIRouter, Depends, File, UploadFile
from app.services.embeddings_service import embed_chunks
from app.services.file_service import extract_text, read_chunks_file, save_chunks_to_file
from app.services.chunking_service import chunk_document

router = APIRouter(prefix="/docs", tags=["Document"])


@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    result = await extract_text(file)

    chunks = chunk_document(
        text=result,
        source=file.filename,
        method="punctuation"
    )

    embeddings = embed_chunks([chunk['text'] for chunk in chunks])

    print(save_chunks_to_file(chunks))

    return {
            "message": "File processed successfully",
            "text_length": len(result),
            "embedding_shape": [
                    len(embeddings),
                    len(embeddings[0])
                ] if embeddings else [0, 0]
        }


@router.get("/chunks/")
async def get_chunks():
    chunks = read_chunks_file()
    return {
            "count": len(chunks),
            "chunks": chunks
        }