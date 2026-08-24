from fastapi import APIRouter, Depends, File, UploadFile
from services.file_service import extract_text

router = APIRouter(prefix="/docs", tags=["Document"])


@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    result = await extract_text(file)
    
    return {
            "message": "File processed successfully",
            "text_length": len(result),
            "preview": result
        }


