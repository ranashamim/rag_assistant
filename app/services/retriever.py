from abc import ABC, abstractmethod

from app.models.models import RetrievalResultModel
from app.services.bm25_service import build_bm25_index, search_bm25
from app.services.embeddings_service import embed_query
from app.services.file_service import read_chunks_file

from app.services.fusion_service import reciprocal_rank_fusion
from app.services.qdrant_service import client

from app.config.settings import settings

class Retriever(ABC):

    @abstractmethod
    async def retrieve(self, query: str, limit: int = 10):
        pass


class DenseRetriever(Retriever):

    async def retrieve(self, query: str, limit: int = 10):

        query_embedding = embed_query(query)
        
        results = client.query_points(
            collection_name= settings.qdrant_collection_name,
            query=query_embedding,
            limit= limit
        )
    
        chunks = read_chunks_file()
    
        chunk_by_id = {
            chunk.chunk_id: chunk
            for chunk in chunks
        }
    
        retrieved_chunks = []
    
        for result in results.points:
            chunk_id = result.payload.get("chunk_id")
            chunk = chunk_by_id.get(chunk_id)
    
            if chunk:
                retrieved_chunks.append(
                    RetrievalResultModel(
                        chunk=chunk,
                        score=result.score
                    )
                )
    
    
        return retrieved_chunks
        

chunks = read_chunks_file()
bm25_index = build_bm25_index(chunks)

class BM25Retriever(Retriever):

    async def retrieve(self, query: str, limit: int = 10):
            results = search_bm25(bm25= bm25_index, query=query, chunks=chunks, limit=limit)
            return results

class HybridRetriever(Retriever):

     async def retrieve(self, query, limit = 10):
            
        bm25 = BM25Retriever()
        dense = DenseRetriever()

        semantic_results = await dense.retrieve(query, limit)
        bm25_results = await bm25.retrieve(query, limit)
        fused_results = reciprocal_rank_fusion([semantic_results, bm25_results])

        return fused_results



