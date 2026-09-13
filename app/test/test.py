
import json

from pydantic import BaseModel

from enum import Enum


class ChunkMethod(str, Enum):
    FIXED = "fixed"
    PUNCTUATION = "punctuation"
    RECURSIVE = "recursive"
    SEMANTIC = "semantic"
    PARENT_CHILD = "parent_child"
    

class ChunkModel(BaseModel):
    chunk_id: str
    text: str
    source: str
    file_type: str
    page_number: int
    chunk_index: int
    method: ChunkMethod
    document_id: str
    parent_chunk_id: str | None = None



def read_chunks_file() -> list[ChunkModel]:
    with open("app/data/chunks/chunks.json", "r", encoding="utf-8") as f:
        chunks = json.load(f)
        
    return [ChunkModel(**chunk) for chunk in chunks]



def get_parent_chunk(child, chunks):

    for chunk in chunks:
        if chunk.chunk_id == child.parent_chunk_id:
            return chunk

    return None

def expand_to_parent(result, chunks):
    child = result.chunk

    parent = get_parent_chunk(child, chunks)

    return {
        "child": child,
        "parent": parent,
        "score": result.score
    }

chunks = read_chunks_file()

children = [
    chunk for chunk in chunks
    if chunk.parent_chunk_id is not None
]

child = children[0]

parent = expand_to_parent(child, chunks)

print("Child:", child.text)
print("Parent:", parent.text)
print("Parent ID:", parent.chunk_id)
print("Child's parent ID:", child.parent_chunk_id)