from abc import ABC, abstractmethod

from app.services.retrieval_service import get_bm25_results, retrieve_chunks


class Retriever(ABC):

    @abstractmethod
    async def retrieve(self, query: str, limit: int = 10):
        pass


class DenseRetriever(Retriever):

    async def retrieve(self, query: str, limit: int = 10):
        results = await retrieve_chunks(query, limit)
        return results
        

class BM25Retriever(Retriever):

    async def retrieve(self, query: str, limit: int = 10):
            results = get_bm25_results(query, limit)
            return results