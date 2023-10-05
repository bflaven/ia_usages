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
cd /Users/brunoflaven/Documents/03_git/BlogArticlesExamples/fastapi_nlp_model/013_fastapi_datacamp/app/


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
from typing import Union
from typing import ClassVar
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None



@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")

def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")

def update_item(item_id: int, item: Item):

    return {"item_name": item.name, "item_id": item_id}

