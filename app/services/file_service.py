from fastapi import UploadFile, HTTPException
from pypdf import PdfReader
import io
import json

from app.models.models import ParsedDocumentModel

async def parse_document(file: UploadFile) -> ParsedDocumentModel:
    docs = {}

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing."
        )

    content = await file.read()

    # TXT files
    if file.filename.lower().endswith(".txt"):
        try:
            docs['filename'] = file.filename
            docs['file_type'] = 'text'
            docs['pages'] = [{'page_number': 1, 'text': content.decode("utf-8")}]

            return ParsedDocumentModel(
                filename= docs['filename'],
                file_type=docs['file_type'],
                pages=docs['pages']
            )
        
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=400,
                detail="TXT file must be UTF-8 encoded."
            )

    # PDF files
    elif file.filename.lower().endswith(".pdf"):
        try:
            docs['filename'] = file.filename
            docs['file_type'] = 'pdf'
            docs['pages'] = []
            
            pdf = PdfReader(io.BytesIO(content))

            for i, page in enumerate(pdf.pages, start=1):
                page_text = page.extract_text()
                docs['pages'].append({'page_number': i, 'text': page_text})
                           

            return ParsedDocumentModel(
                filename= docs['filename'],
                file_type=docs['file_type'],
                pages=docs['pages']
            )

        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error reading PDF: {str(e)}"
            )

    # Unsupported file types
    raise HTTPException(
        status_code=400,
        detail="Only .txt and .pdf files are supported."
    )

def save_chunks_to_file(chunks: list):
    json_str = json.dumps(chunks, indent=4)
    with open("app/data/chunks/chunks.json", "w", encoding="utf-8") as f:
        f.write(json_str)
    
    return "data is written."

def read_chunks_file():
    with open("app/data/chunks/chunks.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    return data
