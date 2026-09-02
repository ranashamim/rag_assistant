from sentence_transformers import SentenceTransformer

from app.config.settings import settings


model = SentenceTransformer(
    settings.embedding_model_name
)


def embed_documents(texts):
    passages = [
        f"passage: {text}"
        for text in texts
    ]

    embeddings = model.encode(
        passages,
        normalize_embeddings=True
    )

    return embeddings.tolist()


def embed_query(query):
    query_text = f"query: {query}"

    embedding = model.encode(
        [query_text],
        normalize_embeddings=True
    )

    return embedding[0].tolist()