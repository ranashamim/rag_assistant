from sentence_transformers import CrossEncoder

model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")

def rerank(query, chunks):
    pairs = [(query, result.chunk.text) for result in chunks]

    scores = model.predict(pairs)

    for result, score in zip(chunks, scores):
        result.score = float(score)

    chunks.sort(key=lambda result: result.score, reverse=True)

    return chunks
