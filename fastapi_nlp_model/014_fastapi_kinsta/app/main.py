#!/usr/bin/python
# -*- coding: utf-8 -*-
#
"""
[ENV]
# Conda Environment
conda create --name fastapi_datacamp
conda info --envs
source activate fastapi_datacamp
conda deactivate


# to export requirements
pip freeze > requirements_fastapi_datacamp.txt

# to install
pip install -r requirements_fastapi_datacamp.txt

# [path]
cd /Users/brunoflaven/Documents/03_git/BlogArticlesExamples/fastapi_nlp_model/014_fastapi_kinsta/app/



# launch the app
uvicorn main:app --reload

# get the docs
http://127.0.0.1:8000/docs/
http://127.0.0.1:8000/redoc

# install

pip install typing
pip install fastapi
pip install pydantic


pip install pycaret



"""
# main.py
from typing import List
from uuid import uuid4
from fastapi import FastAPI
from models import Gender, Role, User, UpdateUser
from uuid import UUID
from fastapi import HTTPException


app = FastAPI()

db: List[User] = [
 User(
 id=uuid4(),
 first_name="John",
 last_name="Doe",
 gender=Gender.male,
 roles=[Role.user],
 ),
 User(
 id=uuid4(),
 first_name="Jane",
 last_name="Doe",
 gender=Gender.female,
 roles=[Role.user],
 ),
 User(
 id=uuid4(),
 first_name="James",
 last_name="Gabriel",
 gender=Gender.male,
 roles=[Role.user],
 ),
 User(
 id=uuid4(),
 first_name="Eunit",
 last_name="Eunit",
 gender=Gender.male,
 roles=[Role.admin, Role.user],
 ),
 User(
 id=uuid4(),
 first_name="Bruno",
 last_name="Flaven",
 gender=Gender.male,
 roles=[Role.admin, Role.user],
 ),
]
@app.get("/")
async def root():
 return {"Hello": "World",}

@app.get("/api/v1/users")
async def get_users():
 return db

@app.post("/api/v1/users")
async def create_user(user: User):
 db.append(user)
 return {"id": user.id}

@app.delete("/api/v1/users/{id}")
async def delete_user(id: UUID):
        for user in db:
         if user.id == id:
            db.remove(user)
            return
         raise HTTPException(
         status_code=404, detail=f"Delete user failed, id {id} not found."
         )
@app.put("/api/v1/users/{id}")
async def update_user(user_update: UpdateUser, id: UUID):
 for user in db:
    if user.id == id:
        if user_update.first_name is not None:
            user.first_name = user_update.first_name
        if user_update.last_name is not None:
            user.last_name = user_update.last_name
        if user_update.gender is not None:
            user.gender = user_update.gender
        if user_update.roles is not None:
            user.roles = user_update.roles
        return user.id
        raise HTTPException(status_code=404, detail=f"Could not find user with id: {id}")

