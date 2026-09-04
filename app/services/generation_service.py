from app.services.llm_service import generate_response
from app.services.router_service import adaptive_retrieve, build_context

def generate_answer(query, context):

    prompt = f"""
            You are a helpful RAG assistant.

            Answer the user's question using only the provided context.
            If the context does not contain enough information to answer,
            say that you don't have enough information.
            When answering, cite the source of the information using
            [Source: filename].

            Use only the provided context.
            Do not invent sources.

            Context:
            {context}

            Question:
            {query}

            Answer:
    
            Return ONLY the answer.
            """

    response = generate_response(prompt=prompt)
    return response

async def answer_query(query):
    result = await adaptive_retrieve(query)
    text_block = build_context(result)
    response = generate_answer(query, text_block)
    return response