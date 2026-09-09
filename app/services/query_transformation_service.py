import json

from app.services.llm_service import generate_response
from app.services.retrieval_service import hybrid_retrieve

def generate_multi_queries(query: str):
    prompt = f"""
    Generate exactly 3 alternative search queries for the user's query.

    All 3 queries must have the same information need as the original query.
    Use different wording or phrasing.
    Do not answer the question.
    Do not introduce a new topic or entity.

    Original query:
    {query}

    Return ONLY a valid JSON array containing exactly 3 strings.
    """

    json_response = generate_response(prompt=prompt)

    # print("MULTI QUERY RAW RESPONSE:", repr(json_response))

    response = json.loads(json_response)

    return response


async def retrieve_multi_query(query: str, final_limit=3):

    multi_queries = generate_multi_queries(query)

    all_chunks = []
    for query_item in multi_queries:
        chunks = await hybrid_retrieve(query_item)

        all_chunks.extend(chunks)

    unique_chunks = {}
    for chunk in all_chunks:
        chunk_id = chunk.chunk.chunk_id
        
        if (
            chunk_id not in unique_chunks
            or chunk.score > unique_chunks[chunk_id].score
        ):
            unique_chunks[chunk_id] = chunk


    return sorted(
        unique_chunks.values(),
        key=lambda chunk: chunk.score,
        reverse=True
    )[:final_limit]

