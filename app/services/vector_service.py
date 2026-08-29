from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

from app.services.chunking_service import chunk_document
from app.services.embeddings_service import embed_chunks
from app.services.file_service import extract_text

client = QdrantClient(
    host="localhost",
    port=6333
)

async def to_db_vector(file, chunking_method):
    text = await extract_text(file)

    chunks = chunk_document(
            text=text,
            source=file.filename,
            method=chunking_method
        )

    embeddings = embed_chunks([chunk['text'] for chunk in chunks])

    points = []

    for chunk, embedding in zip(chunks, embeddings):

        points.append(
            PointStruct(
                id=chunk["chunk_id"],
                vector=embedding,
                payload={      
                    "method": chunking_method,
                    "text": chunk["text"],
                    "source": chunk["source"],
                    "chunk_id": chunk["chunk_id"]
                }
            )
        )

    client.upsert(collection_name="documents", points= points)

    return {
        "chunks_stored": len(points)
    }


