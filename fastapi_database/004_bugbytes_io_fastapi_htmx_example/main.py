#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
conda create --name fastapi_database python=3.9.13
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
cd /Users/brunoflaven/Documents/01_work/blog_articles/fastapi_database/004_bugbytes_io_fastapi_htmx_example/

# LAUNCH THE API
uvicorn main:app
uvicorn main:app --reload

# To see the website
http://127.0.0.1:8000/index/


# Check localhost
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc


Source: https://www.youtube.com/watch?v=8SPF6TBVj28
Code : https://github.com/bugbytes-io/fastapi-htmx-example/tree/master

"""

from typing import Optional
from fastapi import FastAPI, Request, Header, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

# to load the database model
from database import SessionLocal, engine
import models
# from database import models


# from models import Movies
# import models
# from models import Movies

# to load the database
# you should use migration
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
def start_up_populate():
    db = SessionLocal()
    num_films = db.query(models.Films).count()
    if num_films == 0:
        films = [
            {'title': 'Blade Runner', 'director': 'Ridley Scott'},
            {'title': 'Pulp Fiction', 'director': 'Quentin Tarantino'},
            {'title': 'Deer Hunter', 'director': 'Michael Cimino'},
            {'title': 'Spellbound', 'director': 'Alfred Hitchcock'},
            {'title': 'Jules et Jim', 'director': 'François Truffaut'},
            {'title': 'Zabriskie Point',
             'director': 'Michelangelo Antonioni'},
        ]
        for film in films:
            db.add(models.Films(**film))
            db.commit()
    else:
        # print in console
        print(f'{num_films} already in the DB!')


@app.get('/')
def home():
    return {"Welcome here"}

@app.get("/index/", response_class=HTMLResponse)
async def movieList(
    request: Request, 
    hx_request: Optional[str] = Header(None),
    db: Session = Depends(get_db)
    # pagination not in use
    # page: int = 1
    ):

    # N = 2    
    # OFFSET = (page - 1 ) * N
    # films = db.query(models.Films).limit(N)

    films = db.query(models.Films).all()
    # DEBUG
    # print(films)
    # pagination not in use
    # , 'page': page
    context = {"request": request, 'films': films}
    if hx_request:
        return templates.TemplateResponse("partials/table.html", context)
    return templates.TemplateResponse("index.html", context)



