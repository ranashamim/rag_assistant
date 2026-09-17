from app.models.enums import ChunkMethod
from app.services.conversation_service import add_message, get_conversation
from app.services.file_service import read_chunks_file
from app.services.llm_service import generate_response
from app.services.parent_child_service import expand_results, group_by_parent
from app.services.router_service import adaptive_retrieve, build_context, build_parent_child_context

from app.config.settings import settings

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


async def answer_query(query, conversation_id):

    conversation = get_conversation(conversation_id)
    print("Conversation:", conversation)
    
    result = await adaptive_retrieve(query)

    strategy = result["strategy"]
    chunks = result["chunks"]

    if settings.chunk_method == ChunkMethod.PARENT_CHILD:
        print("parent_child")
        all_chunks = read_chunks_file()
        expanded = expand_results(chunks, all_chunks)
        grouped = group_by_parent(expanded)
        context = build_parent_child_context(grouped)
    else:
        print("others")
        context = build_context(chunks)

    
    response = generate_answer(query, context)

    add_message(conversation_id, "user", query)
    add_message(conversation_id, "assistant", response)

    return {
        "answer": response,
        "strategy": strategy
    }