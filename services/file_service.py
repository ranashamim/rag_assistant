from fastapi import UploadFile, HTTPException
from pypdf import PdfReader
import io


async def extract_text(file: UploadFile) -> str:
    """
    Extract text from uploaded TXT or PDF files.

    Args:
        file: FastAPI UploadFile

    Returns:
        str: Extracted text
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing."
        )

    content = await file.read()

    # TXT files
    if file.filename.lower().endswith(".txt"):
        try:
            return content.decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=400,
                detail="TXT file must be UTF-8 encoded."
            )

    # PDF files
    elif file.filename.lower().endswith(".pdf"):
        try:
            pdf = PdfReader(io.BytesIO(content))

            text = ""

            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

            return text

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
   