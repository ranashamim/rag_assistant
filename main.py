from fastapi import FastAPI, UploadFile, File
from routers.documents import router as docs_router

app = FastAPI()

app.include_router(docs_router)

@app.get("/")
async def root():
    return {"message": "RAG Assistant"}
