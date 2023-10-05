#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
conda create --name ner_spacy_fastapi_database python=3.9.13
conda info --envs
source activate ner_spacy_fastapi_database
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n ner_spacy_fastapi_database

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/fastapi_database/007_sql_databases_peewee/

# LAUNCH THE API
uvicorn main:app --reload

# Check localhost
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc


Source: https://fastapi.tiangolo.com/how-to/sql-databases-peewee/

"""



import time
from typing import List

from fastapi import Depends, FastAPI, HTTPException

# from . import crud, database, models, schemas
import crud
import database
import models
import schemas

from database import db_state_default

database.db.connect()
database.db.create_tables([models.User, models.Item])
database.db.close()

app = FastAPI()

sleep_time = 10


async def reset_db_state():
    database.db._state._state.set(db_state_default.copy())
    database.db._state.reset()


def get_db(db_state=Depends(reset_db_state)):
    try:
        database.db.connect()
        yield
    finally:
        if not database.db.is_closed():
            database.db.close()


@app.get('/')
def home():
    return {"Welcome here"}

@app.post("/users/", response_model=schemas.User, dependencies=[Depends(get_db)])
def create_user(user: schemas.UserCreate):
    db_user = crud.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(user=user)


@app.get("/users/", response_model=List[schemas.User], dependencies=[Depends(get_db)])
def read_users(skip: int = 0, limit: int = 100):
    users = crud.get_users(skip=skip, limit=limit)
    return users


@app.get(
    "/users/{user_id}", response_model=schemas.User, dependencies=[Depends(get_db)]
)
def read_user(user_id: int):
    db_user = crud.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post(
    "/users/{user_id}/items/",
    response_model=schemas.Item,
    dependencies=[Depends(get_db)],
)
def create_item_for_user(user_id: int, item: schemas.ItemCreate):
    return crud.create_user_item(item=item, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Item], dependencies=[Depends(get_db)])
def read_items(skip: int = 0, limit: int = 100):
    items = crud.get_items(skip=skip, limit=limit)
    return items


@app.get(
    "/slowusers/", response_model=List[schemas.User], dependencies=[Depends(get_db)]
)
def read_slow_users(skip: int = 0, limit: int = 100):
    global sleep_time
    sleep_time = max(0, sleep_time - 1)
    time.sleep(sleep_time)  # Fake long processing request
    users = crud.get_users(skip=skip, limit=limit)
    return users

