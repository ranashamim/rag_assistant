from pydantic import BaseModel

from app.models.enums import ChunkMethod


class ParsedPage(BaseModel):
    page_number: int
    text: str

class ParsedDocumentModel(BaseModel):
    filename: str
    file_type: str
    pages: list[ParsedPage]


class ChunkModel(BaseModel):
    chunk_id: str
    text: str
    source: str
    file_type: str
    page_number: int
    chunk_index: int
    method: ChunkMethod
    document_id: str

class RetrievalResultModel(BaseModel):
    chunk: ChunkModel
    score: float
