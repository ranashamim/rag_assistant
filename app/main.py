from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.routers.documents import router as docs_router
from app.routers.retrieval_router import router as query_router


from app.services.qdrant_service import create_collection


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_collection()
    yield
    
app = FastAPI(lifespan=lifespan)

app.include_router(docs_router)
app.include_router(query_router)

@app.get("/")
async def root():
    return {"message": "RAG Assistant"}





