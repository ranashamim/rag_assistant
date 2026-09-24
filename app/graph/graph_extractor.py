import json

from app.graph.graph import Graph
from app.graph.graph_models import Entity, ExtractedEntity, Relationship
from app.graph.graph_repository import add_entity, add_relationship
from app.models.models import ChunkModel
from app.services.llm_service import generate_response


class GraphExtractor:

    def extract_entities(self, text: str) -> list[ExtractedEntity]:
        extracted_entities = []

        prompt = f"""
        You are a helpful Graph assistant.

        Extract entities from the provided context.

        For each entity, return:
        - name
        - entity_type

        Return ONLY a JSON list.
        Do not include Markdown.
        Do not include ```json.
        Do not explain anything.
        Use only the supplied text.
        Do not invent entities.
        entity_type should describe what the entity is.

        Context:
        {text}

        Return ONLY the list of entities.
        """

        response = generate_response(prompt=prompt)
        entities = json.loads(response)

        for entity in entities:
            extracted_model = ExtractedEntity(
                name=entity["name"],
                entity_type=entity["entity_type"]
            )
            extracted_entities.append(extracted_model)

        return extracted_entities


    def create_entities(self, extracted_entities: list[ExtractedEntity]) -> list[Entity]:
        entities = []

        for extracted_entity in extracted_entities:
            db_entity = add_entity(name=extracted_entity.name, entity_type=extracted_entity.entity_type)
            graph_entity = Entity(entity_id=db_entity.entity_id, name=db_entity.name, entity_type=db_entity.entity_type)
            entities.append(graph_entity)

        return entities

    def extract_relationships(self, text: str, entities: list[ExtractedEntity]) -> list[Relationship]:
        extracted_relationships = []

        entities_text = "\n".join(
            f"- {entity.name} ({entity.entity_type})"
            for entity in entities
        )

        prompt = f"""
        You are a helpful Graph assistant.

        Extract relationships between the provided entities based only on the provided context.

        Available entities:
        {entities_text}

        For each relationship, return:
        - source
        - target
        - relationship

        Rules:
        - source must be the name of one of the provided entities.
        - target must be the name of one of the provided entities.
        - Do not create new entities.
        - Only extract relationships explicitly supported by the context.
        - relationship should describe the relationship between source and target.
        - Do not invent relationships.
        - If there are no relationships, return an empty JSON list.

        Return ONLY a JSON list.
        Do not include Markdown.
        Do not include ```json.
        Do not explain anything.

        Context:
        {text}

        Return ONLY the list of relationships.
        """

        response = generate_response(prompt=prompt)
        relationships = json.loads(response)

        for relationship in relationships:
            extracted_model = Relationship(
                source=relationship["source"],
                target=relationship["target"],
                relationship=relationship["relationship"]
            )
            extracted_relationships.append(extracted_model)

        return extracted_relationships

    def build_graph(self, graph: Graph, chunk: ChunkModel):
        
        extracted_entities = self.extract_entities(text=chunk.text)
        entities = self.create_entities(extracted_entities=extracted_entities)

        for entity in entities:
            graph.add_entity_if_not_exists(entity)

        extracted_relationships = self.extract_relationships(text=chunk.text, entities=extracted_entities)
        for relationship in extracted_relationships:

            new_relationship = add_relationship(
                source_name=relationship.source,
                target_name=relationship.target,
                relationship=relationship.relationship,
                chunk_id=chunk.chunk_id
            )

            if new_relationship is None:
                continue

            graph_relationship = Relationship(
                source=new_relationship.source_entity_id,
                target=new_relationship.target_entity_id,
                relationship=new_relationship.relationship
            )

            graph.add_relationship(graph_relationship)

        return graph

        