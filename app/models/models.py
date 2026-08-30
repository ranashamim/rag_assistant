from pydantic import BaseModel


class ParsedPage(BaseModel):
    page_number: int
    text: str

class ParsedDocumentModel(BaseModel):
    filename: str
    file_type: str
    pages: list[ParsedPage]
