from rank_bm25 import BM25Okapi


def build_bm25_index(chunks):

    tokens = []

    for chunk in chunks:
        text = chunk["text"]
        tokenize = text.lower().split()
        tokens.append(tokenize)

    bm25 = BM25Okapi(tokens)

    return bm25

def search_bm25(bm25, query, chunks, limit=5):

    query_tokens = query.lower().split()
    scores = bm25.get_scores(query_tokens)
    indexed_scores = list(enumerate(scores))
    top_results = sorted(indexed_scores, key=lambda x: x[1], reverse=True)[:limit]

    related_chunks = []

    for index, score in top_results:
        chunk = chunks[index]
        chunk["bm25_score"] = score
        related_chunks.append(chunk)

    return related_chunks

