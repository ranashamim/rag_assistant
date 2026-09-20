from pydantic import BaseModel



class Entity(BaseModel):
    entity_id: str
    name: str
    entity_type: str


class Relationship(BaseModel):
    source: str
    target: str
    relationship: str