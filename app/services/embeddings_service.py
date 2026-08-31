from sentence_transformers import SentenceTransformer

from app.config.settings import settings


#model = SentenceTransformer("all-MiniLM-L6-v2")
model = SentenceTransformer(settings.embedding_model_name)

def embed_chunks(chunks):
    embeddings = model.encode(chunks)

    return embeddings.tolist()



