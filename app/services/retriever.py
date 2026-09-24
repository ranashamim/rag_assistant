from abc import ABC, abstractmethod

from app.graph.graph_extractor import GraphExtractor
from app.graph.graph_repository import get_entity_by_id, get_entity_by_name, get_relationships, traverse_from_database
from app.models.enums import ChunkMethod
from app.models.models import GraphRetrievalResultModel, RetrievalResultModel
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
            collection_name=settings.qdrant_collection_name,
            query=query_embedding,
            limit=limit
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
                retrieval_result = RetrievalResultModel(
                    chunk=chunk,
                    score=result.score
                )

                retrieved_chunks.append(retrieval_result)

        return retrieved_chunks


class BM25Retriever(Retriever):

    async def retrieve(self, query: str, limit: int = 10):
        
        chunks = read_chunks_file()

        if not chunks:
            return []
        
        if settings.chunk_method == ChunkMethod.PARENT_CHILD:
            chunks = [
                chunk
                for chunk in chunks
                if chunk.parent_chunk_id is not None
            ]

        bm25_index = build_bm25_index(chunks)
        results = search_bm25(
            bm25=bm25_index,
            query=query,
            chunks=chunks,
            limit=limit
        )

        return results


class HybridRetriever(Retriever):

    async def retrieve(self, query, limit=10):

        bm25 = BM25Retriever()
        dense = DenseRetriever()

        semantic_results = await dense.retrieve(query, limit)
        bm25_results = await bm25.retrieve(query, limit)

        fused_results = reciprocal_rank_fusion(
            [semantic_results, bm25_results]
        )

        return fused_results

class GraphRetriever(Retriever):

    async def retrieve(self, query: str, limit: int = 10):
        retrieved_results = []

        graph_extractor = GraphExtractor()

        entities = graph_extractor.extract_entities(
            text=query
        )

        if not entities:
            return []

        unique_entities = {}

        for entity in entities:
            key = entity.name.lower()

            if key not in unique_entities:
                unique_entities[key] = entity

        entities = list(unique_entities.values())

        for entity in entities:

            db_entity = get_entity_by_name(entity.name)

            if db_entity is None:
                continue

            traversal_results = traverse_from_database(
                entity_id=db_entity.entity_id,
                max_hops=2
            )

            for current_entity, relationship, neighbor in traversal_results:

                if relationship.source_entity_id == current_entity.entity_id:
                    source = current_entity
                    target = neighbor
                else:
                    source = neighbor
                    target = current_entity

                result = GraphRetrievalResultModel(
                    source_name=source.name,
                    source_type=source.entity_type,
                    target_name=target.name,
                    target_type=target.entity_type,
                    relationship=relationship.relationship
                )

                retrieved_results.append(result)

                if len(retrieved_results) >= limit:
                    return retrieved_results

        return retrieved_results