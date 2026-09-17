
from qdrant_client.models import PointStruct

import uuid

from app.models.enums import ChunkMethod
from app.services.chunking_service import chunk_document
from app.services.embeddings_service import embed_documents
from app.services.file_service import delete_chunks_by_source, parse_document, save_chunks_to_file

from app.config.settings import settings

from app.services.qdrant_service import client, delete_vectors_by_source


async def to_db_vector(file, chunking_method):
    document_id = str(uuid.uuid4())

    parsed_doc = await parse_document(file)

    delete_vectors_by_source(parsed_doc.filename)
    delete_chunks_by_source(parsed_doc.filename)

    chunks = []
    for page in parsed_doc.pages:
        page_chunks = chunk_document(text= page.text, page_number= page.page_number, file_type= parsed_doc.file_type, document_id= document_id, source=parsed_doc.filename, method=chunking_method)
        chunks.extend(page_chunks)

    if chunking_method == ChunkMethod.PARENT_CHILD:
        retrieval_chunks = [ chunk for chunk in chunks if chunk.parent_chunk_id is not None]
    else:
        retrieval_chunks = chunks

    save_chunks_to_file(chunks)
    
    embeddings = embed_documents([chunk.text for chunk in retrieval_chunks])

    points = []

    for chunk, embedding in zip(retrieval_chunks, embeddings):
        print("Points:", len(points))
        points.append(
            PointStruct(
                id=chunk.chunk_id,
                vector=embedding,
                payload={      
                    "method": chunking_method,
                    "text": chunk.text,
                    "source": chunk.source,
                    "chunk_id": chunk.chunk_id,
                    "file_type": chunk.file_type,
                    "page_number": chunk.page_number,
                    "chunk_index": chunk.chunk_index, 
                    "document_id": chunk.document_id,
                    "parent_chunk_id": chunk.parent_chunk_id
                }
            )
        )

    client.upsert(settings.qdrant_collection_name, points= points)

    print("All chunks:", len(chunks))
    print("Retrieval chunks:", len(retrieval_chunks))

    return {
        "chunks_stored": len(points)
    }


