def reciprocal_rank_fusion(result_lists, k=60):

    fused_results = {}

    for results in result_lists:

        for rank, chunk in enumerate(results, start=1):

            chunk_id = chunk.chunk.chunk_id
            fusion_score = 1 / (k + rank)

            if chunk_id not in fused_results:
                fused_results[chunk_id] = {
                    "chunk": chunk,
                    "fusion_score": fusion_score
                }
            else:
                fused_results[chunk_id]["fusion_score"] += fusion_score



    sorted_results = sorted(
        fused_results.items(),
        key=lambda x: x[1]["fusion_score"],
        reverse=True
    )

    fused_chunks = []

    for chunk_id, data in sorted_results:
        result = data["chunk"]
        result.score = data["fusion_score"]
        fused_chunks.append(result)

    return fused_chunks
