from app.services.llm_service import generate_response


def route_query(query: str):

    prompt = f"""
Classify the following user query.

Query: {query}

Choose exactly one query_type:
- simple
- complex
- ambiguous

Choose exactly one strategy:
- normal_retrieval
- decomposition
- rewrite

Return ONLY valid JSON in this format:
{{
    "query_type": "...",
    "strategy": "..."
}}
"""

    classified_query = generate_response(prompt=prompt)

    return classified_query


