from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

import uuid

from app.services.chunking_service import chunk_document
from app.services.embeddings_service import embed_documents
from app.services.file_service import parse_document

from app.config.settings import settings

from app.services.qdrant_service import client


async def to_db_vector(file, chunking_method):
    document_id = str(uuid.uuid4())

    parsed_doc = await parse_document(file)

    chunks = []
    for page in parsed_doc.pages:
        page_chunks = chunk_document(text= page.text, page_number= page.page_number, file_type= parsed_doc.file_type, document_id= document_id, source=parsed_doc.filename, method=chunking_method)
        chunks.extend(page_chunks)

    embeddings = embed_documents([chunk['text'] for chunk in chunks])

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
                    "chunk_id": chunk["chunk_id"],
                    "file_type": chunk['file_type'],
                    "page_number": chunk['page_number'],
                    "chunk_index": chunk['chunk_index'], 
                    "document_id": chunk["document_id"]
                }
            )
        )

    client.upsert(settings.qdrant_collection_name, points= points)

    return {
        "chunks_stored": len(points)
    }


