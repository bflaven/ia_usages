from typing import List
from pydantic import BaseModel


class Content(BaseModel):
    post_url: str
    content: str


class Payload(BaseModel):
    data: List[Content]


class SingleEntity(BaseModel):
    text: str
    entity_type: str


class Entities(BaseModel):
    post_url: str
    entities: List[SingleEntity]