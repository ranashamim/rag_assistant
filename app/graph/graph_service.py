from app.graph.graph import Graph
from app.graph.graph_extractor import GraphExtractor
from app.models.models import ChunkModel
from app.models.enums import ChunkMethod

from app.database.database import SessionLocal
from app.database.models import Entity as DBEntity
from app.database.models import GraphRelationship
from sqlalchemy import select

def test_build_graph():

    chunk = ChunkModel(
        chunk_id="test-chunk-1",
        text=(
            "Microsoft acquired GitHub in 2018. "
            "GitHub created GitHub Copilot."
        ),
        source="test.txt",
        file_type="txt",
        page_number=1,
        chunk_index=0,
        method=ChunkMethod.FIXED,
        document_id="test-document-1"
    )

    graph = Graph()
    extractor = GraphExtractor()

    graph1 = extractor.build_graph(
        graph=graph,
        chunk=chunk
    )


    print("\nENTITIES:")
    for entity in graph1.entities.values():
        print(
            entity.entity_id,
            entity.name,
            entity.entity_type
        )

    print("\nRELATIONSHIPS:")
    for relationship in graph1.relationships:
        print(
            relationship.source,
            relationship.target,
            relationship.relationship
        )

    db = SessionLocal()

    entities = db.execute(
        select(DBEntity)
    ).scalars().all()

    relationships = db.execute(
        select(GraphRelationship)
    ).scalars().all()

    print("\nDATABASE ENTITIES:")
    for entity in entities:
        print(
            entity.entity_id,
            entity.name,
            entity.entity_type
        )

    print("\nDATABASE RELATIONSHIPS:")
    for relationship in relationships:
        print(
            relationship.source_entity_id,
            relationship.target_entity_id,
            relationship.relationship,
            relationship.chunk_id
        )

    db.close()

if __name__ == "__main__":
    test_build_graph()