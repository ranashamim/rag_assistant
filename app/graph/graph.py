from app.graph.graph_models import Entity, Relationship


class Graph:

    def __init__(self):
        self.entities = {}
        self.relationships = []

    def add_entity(self, entity: Entity):
        self.entities[entity.entity_id] = entity

    def add_relationship(self, relationship: Relationship):
        self.relationships.append(relationship)

    def get_entity(self, entity_id: str):
        return self.entities.get(entity_id)

    def get_entity_by_name(self, name: str):
        for entity in self.entities.values():
            if entity.name == name:
                return entity
        return None


    def get_related_entities(self, entity_id: str):
        result = []

        for relationship in self.relationships:
            if relationship.source == entity_id:
                result.append(relationship.target)

            elif relationship.target == entity_id:
                result.append(relationship.source)

        return result

    def get_related_relationships(self, entity_id: str):
        result = []

        for relationship in self.relationships:
            if relationship.source == entity_id:
                result.append(relationship)

            elif relationship.target == entity_id:
                result.append(relationship)

        return result

    def traverse(self, entity_id: str, max_hops: int = 2):
        frontier = [entity_id]
        visited = {entity_id}
        results = []

        while frontier and max_hops > 0:
            next_frontier = []

            for current in frontier:
                related_entities = self.get_related_entities(current)

                for entity in related_entities:
                    if entity not in visited:
                        visited.add(entity)
                        results.append(self.get_entity(entity_id=entity))
                        next_frontier.append(entity)

            frontier = next_frontier
            max_hops -= 1

        return results

    def add_relationship_by_name(self, source_name: str, target_name: str, relationship: str):
        source = self.get_entity_by_name(name=source_name)
        target = self.get_entity_by_name(name=target_name)

        if source is None or target is None:
            return

        new_relationship = Relationship(
            source=source.entity_id,
            target=target.entity_id,
            relationship=relationship
        )

        self.add_relationship(new_relationship)

    def add_entity_if_not_exists(self, entity: Entity) -> Entity:
        for existing_entity in self.entities.values():
            if entity.name.lower() == existing_entity.name.lower():
                return existing_entity

        self.add_entity(entity=entity)
        return entity    