
from app.graph.graph_models import Entity, Relationship


microsoft = Entity(
    entity_id="1",
    name="Microsoft",
    entity_type="company"
)

github = Entity(
    entity_id="2",
    name="GitHub",
    entity_type="company"
)

copilot = Entity(
    entity_id="3",
    name="Copilot",
    entity_type="product"
)

r1 = Relationship(
    source=microsoft.entity_id,
    target=github.entity_id,
    relationship="acquired"
)

r2 = Relationship(
    source=github.entity_id,
    target=copilot.entity_id,
    relationship="created"
)

entities = [microsoft, github, copilot]
relationships = [r1, r2]


def get_related_entities(entity_id, relationships):
    result = []

    for relationship in relationships:
        if relationship.source == entity_id:
            result.append(relationship.target)

        if relationship.target == entity_id:
            result.append(relationship.source)

    return result

def traverse_graph(entity_id, relationships, max_hops=2):
    ...
    
    
    