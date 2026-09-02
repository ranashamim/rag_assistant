from sentence_transformers import CrossEncoder

model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")


def rerank(query, chunks):
    pairs = [
        (query, chunk["text"])
        for chunk in chunks
    ]

    scores = model.predict(pairs)

    for chunk, score in zip(chunks, scores):
        chunk["rerank_score"] = float(score)

    chunks.sort(
        key=lambda chunk: chunk["rerank_score"],
        reverse=True
    )

    return chunks

