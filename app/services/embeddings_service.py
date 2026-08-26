from sentence_transformers import SentenceTransformer

#model = SentenceTransformer("all-MiniLM-L6-v2")
model = SentenceTransformer("intfloat/multilingual-e5-large")

def embed_chunks(chunks):
    embeddings = model.encode(chunks)

    return embeddings.tolist()



