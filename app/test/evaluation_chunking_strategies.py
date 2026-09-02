
import json

from app.services.retrieval_service import retrieve_chunks
from app.services.vector_service import to_db_vector


def read_queries():
    with open("app/data/evaluation_queries.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    return data

def save_to_file(answer: list):
    json_str = json.dumps(answer, indent=4)
    with open("app/data/evaluation_answers.json", "a", encoding="utf-8") as f:
        f.write(json_str)
    
    return "data is written."

async def evaluation():
    queries = read_queries()

    answer = []
    for query in queries:
        answer.append(query)
        answer.extend(await retrieve_chunks(query=query['query']))

    save_to_file(answer= answer)

