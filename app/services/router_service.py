from app.models.models import GraphRetrievalResultModel, RetrievalResultModel
from app.services.llm_service import generate_response

import json

from app.services.query_transformation_service import retrieve_multi_query
from app.services.retrieval_service import hybrid_retrieve
from app.services.retriever import GraphRetriever

def route_query(query: str):

    prompt = f"""
    Classify the following user query.

    Query: {query}

    Choose exactly one query_type:
    - simple: a clear, self-contained question that can be answered using normal retrieval.
    - complex: a question requiring multiple pieces of information, comparison, or multiple reasoning steps.
    - ambiguous: a question that is unclear or depends on missing context.
    - broad: a clear question where different formulations or terminology may retrieve different relevant information.
    - graph: a question that depends on relationships between entities,such as who acquired whom, who created what, what is connected to what,
      or questions requiring traversal across multiple entity relationships.

    Choose the strategy based on these rules:
    - simple -> normal_retrieval
    - complex -> decomposition
    - ambiguous -> rewrite
    - broad -> multi_query
    - graph -> graph_retrieval
    
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

    result = json.loads(response)

    if isinstance(result, str):
        result = json.loads(result)

    return result


async def retrieve_decomposed(query: str, final_limit=3):

    sub_queries = decompose_query(query)

    all_chunks = []

    for sub_query in sub_queries:
        chunks = await hybrid_retrieve(
            sub_query,
            candidate_limit=10
        )

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


def rewrite_query(query: str, history: str = ""):

    prompt = f"""
    Rewrite the user's query into a clear, self-contained question
    for document retrieval.

    IMPORTANT:
    The current query may contain references such as:
    "it", "this", "that", "they", "these", "those", "its", or similar
    words that refer to something mentioned earlier in the conversation.

    If such a reference exists, identify what it refers to using the
    conversation history and replace the reference with the specific topic.

    The rewritten query MUST be understandable without reading
    the conversation history.

    Use ONLY information explicitly present in the current query
    and conversation history.

    Do NOT invent any topic, entity, or subject.

    If the query is already self-contained, keep its meaning unchanged.

    If the reference cannot be resolved from the conversation history,
    return the original query unchanged.

    Conversation history:
    {history}

    Current user query:
    {query}

    Return ONLY the rewritten question.
    """

    response = generate_response(prompt=prompt)

    return response.strip()


async def adaptive_retrieve(query: str, history: str = ""):

    routing = route_query(query)
    strategy = routing["strategy"]
    query_type = routing["query_type"]

    if strategy == "normal_retrieval":
        print("***************")
        print(strategy)
        reranked_chunks = await hybrid_retrieve(
            query,
            candidate_limit=10
        )
    
    elif strategy == "decomposition":
        print("***************")
        print(strategy)
        reranked_chunks = await retrieve_decomposed(query)

    elif strategy == "rewrite":
        print("***************")
        print(strategy)
        rewritten_query = rewrite_query(query, history)

    
        print("REWRITTEN QUERY:", rewritten_query)

        reranked_chunks = await hybrid_retrieve(
            rewritten_query,
            candidate_limit=10
        )


    elif strategy == "multi_query":
        print("***************")
        print(strategy)
        reranked_chunks = await retrieve_multi_query(query)

    elif strategy == "graph_retrieval":
        print("***************")
        print(strategy)

        graph_retriever = GraphRetriever()

        graph_results = await graph_retriever.retrieve(
            query,
            limit=10
        )
        reranked_chunks = graph_results


    return {
        "query_type": query_type,
        "strategy": strategy,
        "chunks": reranked_chunks
    }

def build_context(results):

    context_parts = []

    for result in results:

        if isinstance(result, RetrievalResultModel):
            context_parts.append(
                f"Source: {result.chunk.source}\n"
                f"Content: {result.chunk.text}"
            )

        elif isinstance(result, GraphRetrievalResultModel):
            context_parts.append(
                f"Graph relationship:\n"
                f"{result.source_name} "
                f"({result.source_type}) "
                f"{result.relationship} "
                f"{result.target_name} "
                f"({result.target_type})"
            )

    return "\n\n".join(context_parts)


def build_parent_child_context(results):
    context_parts = []

    for result in results:
        child_texts = "\n".join(
            child.text
            for child in result.children
        )

        context_parts.append(
            f"Source: {result.parent.source}\n"
            f"Parent Text:\n{result.parent.text}\n"
            f"Relevant Child Texts:\n{child_texts}"
        )

    return "\n\n".join(context_parts)