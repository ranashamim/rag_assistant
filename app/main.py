from fastapi import FastAPI
from app.routers.documents import router as docs_router
from app.routers.retrieval_router import router as query_router

app = FastAPI()

app.include_router(docs_router)
app.include_router(query_router)

@app.get("/")
async def root():
    return {"message": "RAG Assistant"}
