from datetime import datetime
import uuid

from app.database.database import SessionLocal
from app.database.models import Entity, GraphRelationship

from sqlalchemy import func, select

from app.graph.graph import Graph


def add_entity(name, entity_type):
    db = SessionLocal()

    try:
        statement = select(Entity).where(
            func.lower(Entity.name) == name.lower()
        )

        result = db.execute(statement)
        entity = result.scalar_one_or_none()

        if entity:
            return entity

        new_entity = Entity(
            entity_id=str(uuid.uuid4()),
            name=name,
            entity_type=entity_type,
            created_at=datetime.now()
        )

        db.add(new_entity)
        db.commit()

        return new_entity

    finally:
        db.close()

def add_relationship(source_name, target_name, relationship, chunk_id):
    db = SessionLocal()

    try:
        # get source entity
        statement_source = select(Entity).where(
            func.lower(Entity.name) == source_name.lower()
        )
        result = db.execute(statement_source)
        entity_source = result.scalar_one_or_none()

        # get target entity
        statement_target = select(Entity).where(
            func.lower(Entity.name) == target_name.lower()
        )
        result = db.execute(statement_target)
        entity_target = result.scalar_one_or_none()

        if entity_source is None or entity_target is None:
            return None

        # checking if relationship exists or not
        statement_relationship = select(GraphRelationship).where(
            GraphRelationship.source_entity_id == entity_source.entity_id,
            GraphRelationship.target_entity_id == entity_target.entity_id,
            GraphRelationship.relationship == relationship
        )

        result = db.execute(statement_relationship)
        relation = result.scalar_one_or_none()

        if relation:
            return relation

        new_relationship = GraphRelationship(
            source_entity_id=entity_source.entity_id,
            target_entity_id=entity_target.entity_id,
            relationship=relationship,
            chunk_id=chunk_id,
            created_at=datetime.now()
        )

        db.add(new_relationship)
        db.commit()

        return new_relationship

    finally:
        db.close()


def save_graph(graph: Graph):
    db = SessionLocal()

    try:
        entity_id_map = {}

        # 1. Save entities
        for graph_entity in graph.entities.values():

            statement = select(Entity).where(
                func.lower(Entity.name) == graph_entity.name.lower()
            )

            result = db.execute(statement)
            db_entity = result.scalar_one_or_none()

            if db_entity is None:
                db_entity = Entity(
                    entity_id=str(uuid.uuid4()),
                    name=graph_entity.name,
                    entity_type=graph_entity.entity_type,
                    created_at=datetime.now()
                )

                db.add(db_entity)
                db.flush()

            entity_id_map[graph_entity.entity_id] = db_entity.entity_id

        # 2. Save relationships
        for graph_relationship in graph.relationships:

            source_id = entity_id_map.get(
                graph_relationship.source
            )

            target_id = entity_id_map.get(
                graph_relationship.target
            )

            if source_id is None or target_id is None:
                continue

            statement = select(GraphRelationship).where(
                GraphRelationship.source_entity_id == source_id,
                GraphRelationship.target_entity_id == target_id,
                GraphRelationship.relationship == graph_relationship.relationship
            )

            result = db.execute(statement)
            existing_relationship = result.scalar_one_or_none()

            if existing_relationship is not None:
                continue

            db_relationship = GraphRelationship(
                source_entity_id=source_id,
                target_entity_id=target_id,
                relationship=graph_relationship.relationship,
                chunk_id="unknown",
                created_at=datetime.now()
            )

            db.add(db_relationship)

        # 3. Commit everything once
        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()