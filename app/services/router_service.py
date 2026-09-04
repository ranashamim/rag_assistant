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

def rewrite_query(query: str, context: str = ""):

    prompt = f"""
        Rewrite the user's query into a clear, self-contained question
        for document retrieval.

        Use ONLY information explicitly present in the user query
        and the provided context.

        Do NOT invent a topic, entity, or subject that is not present
        in the query or context.

        If the query cannot be rewritten without missing information,
        return the original query unchanged.

        Context:
        {context}

        User query:
        {query}

        Return ONLY the rewritten question.
        """

    response = generate_response(prompt=prompt)

    return response.strip()


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
    elif strategy == "decomposition":
        reranked_chunks = await retrieve_decomposed(query)

        return reranked_chunks

    elif strategy == "rewrite":
        rewritten_query = rewrite_query(query)

        reranked_chunks = await rerank_retrieved_chunks(
            rewritten_query,
            candidate_limit=10,
            rerank_limit=3
        )

        return reranked_chunks

    return {
        "strategy": strategy,
        "message": "Strategy not implemented yet"
    }

def build_context(chunks):

    context_parts = []

    for chunk in chunks:
        context_parts.append(
            f"Source: {chunk['source']}\n"
            f"Content: {chunk['text']}"
        )

    return "\n\n".join(context_parts)
