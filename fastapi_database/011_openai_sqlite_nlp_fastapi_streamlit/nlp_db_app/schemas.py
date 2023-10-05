# schemas.py

from pydantic import BaseModel

class PostBase(BaseModel):
    post_title: str
    post_body: str
    post_origin_id: int
    api_result: str

class PostCreate(PostBase):
    pass

class Post(PostBase):
    post_id: int

    class Config:
        orm_mode = True
