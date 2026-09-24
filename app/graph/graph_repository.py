from datetime import datetime
import uuid

from app.database.database import SessionLocal
from app.database.models import Entity, GraphRelationship

from sqlalchemy import func, select


def add_entity(name, entity_type):
    db = SessionLocal()
    
    statement = select(Entity).where(
        func.lower(Entity.name) == name.lower()
    )
    result = db.execute(statement)
    entity = result.scalar_one_or_none()

    if entity:
        db.close()
        return entity

    new_entity = Entity(
        entity_id=str(uuid.uuid4()),
        name=name,
        entity_type=entity_type,
        created_at=datetime.now()
    )

    db.add(new_entity)
    db.commit()
    db.close()

    return new_entity


def add_relationship(source_name, target_name, relationship, chunk_id):
    db = SessionLocal()

    #get source entity
    statement_source = select(Entity).where(
        func.lower(Entity.name) == source_name.lower()
    )
    result = db.execute(statement_source)
    entity_source = result.scalar_one_or_none()

    #get target entity
    statement_target = select(Entity).where(
        func.lower(Entity.name) == target_name.lower()
    )
    result = db.execute(statement_target)
    entity_target = result.scalar_one_or_none()

    #checking if relationship exist or not
    if(entity_source and entity_target):
        statement_relationship = select(GraphRelationship).where(
            GraphRelationship.source_entity_id == entity_source.entity_id,
            GraphRelationship.target_entity_id == entity_target.entity_id,
            GraphRelationship.relationship == relationship
        )

        result = db.execute(statement_relationship)
        relation = result.scalar_one_or_none()

        if relation:
            db.close()
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
        db.close()

        return new_relationship
    
    db.close()
    return None

