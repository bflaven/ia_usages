# crud.py
from sqlalchemy.orm import Session

from . import models, schemas
# import models
# import schemas

def create_post(db: Session, post: models.Post):
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.post_id == post_id).first()

def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Post).offset(skip).limit(limit).all()

