from app.services.llm_service import generate_response

import json

from app.services.retrieval_service import rerank_retrieved_chunks

def route_query(query: str):

    prompt = f"""
    Classify the following user query.

    Query: {query}

    Choose exactly one query_type:
    - simple: a clear, self-contained question that can be answered using normal retrieval.
    - complex: a question requiring multiple pieces of information, comparison, or multiple reasoning steps.
    - ambiguous: a question that is unclear or depends on missing context.

    Choose the strategy based on these rules:
    - simple -> normal_retrieval
    - complex -> decomposition
    - ambiguous -> rewrite

    Return ONLY valid JSON in this exact format:
    {{
        "query_type": "...",
        "strategy": "..."
    }}
    """

    classified_query = generate_response(prompt=prompt)
    parsed_classified_query = json.loads(classified_query)

    return parsed_classified_query

def decompose_query(query: str):

    prompt = f"""
        Break the following complex question into smaller, independent questions
        that can each be answered using document retrieval.

        Question:
        {query}

        Return ONLY a valid JSON array of strings.

        Example:
        ["question 1", "question 2", "question 3"]
        """

    response = generate_response(prompt=prompt)

    print("DECOMPOSITION RESPONSE:")
    print(repr(response))

    result = json.loads(response)

    if isinstance(result, str):
        result = json.loads(result)

    return result


async def retrieve_decomposed(query: str):

    sub_queries = decompose_query(query)

    all_chunks = []

    for sub_query in sub_queries:
        chunks = await rerank_retrieved_chunks(
            sub_query,
            candidate_limit=10,
            rerank_limit=3
        )

        all_chunks.extend(chunks)

    unique_chunks = {}

    for chunk in all_chunks:
        chunk_id = chunk["chunk_id"]

        if (
            chunk_id not in unique_chunks
            or chunk["rerank_score"] > unique_chunks[chunk_id]["rerank_score"]
        ):
            unique_chunks[chunk_id] = chunk

    return sorted(
        unique_chunks.values(),
        key=lambda chunk: chunk["rerank_score"],
        reverse=True
    )



async def adaptive_retrieve(query: str):

    routing = route_query(query)
    strategy = routing["strategy"]

    if strategy == "normal_retrieval":
        reranked_chunks = await rerank_retrieved_chunks(
            query,
            candidate_limit=10,
            rerank_limit=3
        )
        return reranked_chunks

    return {
        "strategy": strategy,
        "message": "Strategy not implemented yet"
    }
