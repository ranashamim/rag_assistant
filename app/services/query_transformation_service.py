import json

from app.services.llm_service import generate_response

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

    response = json.loads(json_response) 
    
    return response
