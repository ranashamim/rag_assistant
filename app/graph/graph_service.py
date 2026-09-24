import asyncio

from app.services.retriever import GraphRetriever


async def main():
    retriever = GraphRetriever()

    results = await retriever.retrieve(
        query="What companies did Microsoft acquire?"
    )

    for entity in results:
        print(
            entity.source_name,
            "|",
            entity.source_type,
            "|",
            entity.target_name,
            "|",
            entity.target_type,
            "|",
            entity.relationship
        )


asyncio.run(main())

    