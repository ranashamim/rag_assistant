def reciprocal_rank_fusion(result_lists, k=60):

    fused_results = {}

    for results in result_lists:

        for rank, chunk in enumerate(results, start=1):

            chunk_id = chunk["chunk_id"]
            fusion_score = 1 / (k + rank)

            if chunk_id not in fused_results:
                fused_results[chunk_id] = {
                    "chunk": chunk,
                    "fusion_score": fusion_score
                }
            else:
                fused_results[chunk_id]["fusion_score"] += fusion_score

    print("FUSED RESULTS:")
    print(fused_results)

    sorted_results = sorted(
        fused_results.items(),
        key=lambda x: x[1]["fusion_score"],
        reverse=True
    )

    fused_chunks = []

    for chunk_id, data in sorted_results:
        chunk = data["chunk"]
        chunk["fusion_score"] = data["fusion_score"]
        fused_chunks.append(chunk)

    return fused_chunks

semantic_results = [
    {
        "chunk_id": "chunk_001",
        "text": "...",
        "score": 0.91
    },
    {
        "chunk_id": "chunk_003",
        "text": "...",
        "score": 0.87
    },
    {
        "chunk_id": "chunk_002",
        "text": "...",
        "score": 0.84
    },
]

bm25_results = [
    {
        "chunk_id": "chunk_002",
        "text": "...",
        "bm25_score": 8.5
    },
    {
        "chunk_id": "chunk_001",
        "text": "...",
        "bm25_score": 7.2
    },
    {
        "chunk_id": "chunk_004",
        "text": "...",
        "bm25_score": 5.1
    },
]
print("SEMANTIC:")
print(semantic_results)

print("BM25:")
print(bm25_results)

result = reciprocal_rank_fusion(
    [semantic_results, bm25_results]
)

print(result)