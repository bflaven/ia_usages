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
cd /Users/brunoflaven/Documents/03_git/BlogArticlesExamples/fastapi_database/011_openai_sqlite_nlp_fastapi_streamlit/

# LAUNCH THE API
uvicorn nlp_db_app.main:app --reload



# Check localhost
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc


- requirements for spacy
pip install spacy 


- requirements for Spacy
python -m spacy download en_core_web_sm
python -m spacy download es_core_news_sm
python -m spacy download fr_core_news_sm
python -m spacy download ru_core_news_sm

# check install
python -m spacy validate

"""
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from . import crud, models, schemas
# import crud
# import models
# import schemas
from .database import SessionLocal, engine

from fastapi import FastAPI, Depends, HTTPException, Body
# from sqlalchemy.orm import Session
# from sqlalchemy import Session
# from . import crud, models, database, schemas
from typing import List
import spacy

import srsly

example_request = srsly.read_json("data/example_request.json")


# tags_metadata
tags_metadata = [
    {
        'name': 'home',
        'description': 'No place like home'
    },
    {
        'name': 'healthcheck',
        'description': 'It basically sends a GET request to the route & hopes to get a "200"'
    },
    {
        'name': 'summary',
        'description': 'For the moment, a fake endpoint. It waits for the function and the summarization logic but it should enable to make a summary from a text.'
    },
    {
        'name': 'keywords',
        'description': 'Takes in a string and returns the main tags of the text.'
    },
    {
        'name': 'entities',
        'description': 'Takes in a string and returns entities (NER). Named Entity Recognition is a standard NLP problem which involves spotting named entities (people, places, organizations etc.) from a chunk of text, and classifying them into a predefined set of categories.'
    },
    {
        'name': 'edit_post',
        'description': 'Edit a specific Post stored in the DB.'
    },
    {
        'name': 'list_post',
        'description': 'List all the Posts stored in the DB.'
    }
    
    
]

models.Base.metadata.create_all(bind=engine)

app = FastAPI(    
    title="TrattorIA",
    description="""Obtain different features in NLP from Spacy in FR, ES, EN, RU. The result, this time is saved in a DB.""",
    openapi_tags=tags_metadata,
    version="2.0",
    )

# Load Spacy models for different languages
nlp = {
    "en": spacy.load("en_core_web_sm"),
    "fr": spacy.load("fr_core_news_sm"),
    "es": spacy.load("es_core_news_sm"),
    "ru": spacy.load("ru_core_news_sm"),
}


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/', include_in_schema=False, tags=['home'])
def home():
    # return {"nlp_db_app - Welcome here - Benvenidos aqui - Добро пожаловать - Bienvenue ici"}
    return RedirectResponse(f"/docs")

@app.get('/healthcheck', tags=['healthcheck'])
def perform_healthcheck():
    '''
    It basically sends a GET request to the route & hopes to get a "200"
    response code. Failing to return a 200 response code just enables
    the GitHub Actions to rollback to the last version the project was
    found in a "working condition". It acts as a last line of defense in case something goes south.
    Additionally, it also returns a JSON response in the form of:
    {
        'healtcheck': 'Everything OK!'
    }
    '''
    return {'healthcheck': 'Everything OK!'}


# NER endpoint
@app.post("/entities/{lang}", response_model=schemas.Post, tags=['entities'])
async def entities(
    lang: str,
    post_data: schemas.PostCreate = Body(..., example=example_request),
    db: Session = Depends(get_db),
):
    if lang not in nlp:
        raise HTTPException(status_code=400, detail="Language not supported")

    nlp_model = nlp[lang]
    doc = nlp_model(post_data.post_body)

    # Extract named entities and update the keywords_ner field
    named_entities = [ent.text for ent in doc.ents]
    post_data.api_result = ", ".join(named_entities)

    # Create a Post record with the extracted named entities
    post = models.Post(**post_data.dict())

    # Save the Post record to the database
    crud.create_post(db, post)

    return post

# Keywords endpoint
@app.post("/keywords/{lang}", response_model=schemas.Post, tags=['keywords'])
async def get_keywords(
    lang: str,
    post_data: schemas.PostCreate = Body(..., example=example_request),
    db: Session = Depends(get_db),
):
    nlp_model = nlp[lang]
    doc = nlp_model(post_data.post_body)



    # Create a dictionary to store the frequency of each keyword
    keyword_freq = {}

    # Iterate through tokens and count keyword frequency
    for token in doc:
        # Filter out stopwords and punctuation
        if not token.is_stop and not token.is_punct:
            lemma = token.lemma_.lower()  # Convert to lowercase
            keyword_freq[lemma] = keyword_freq.get(lemma, 0) + 1

    # Sort keywords by frequency in descending order
    sorted_keywords = sorted(keyword_freq.items(), key=lambda x: x[1], reverse=True)

    # Extract the top 10 keywords (you can change this number)
    top_keywords = [keyword for keyword, freq in sorted_keywords[:10]]
    post_data.api_result = ", ".join(top_keywords)

    # Create a Post record with the extracted top_keywords
    post = models.Post(**post_data.dict())

    # Save the Post record to the database
    crud.create_post(db, post)

    # DEBUG 
    # return {"keywords": top_keywords}
    # return {"post": post}

    return post
# lang: str,
# post_data: schemas.PostCreate = Body(..., example=example_request),
# db: Session = Depends(get_db),

@app.post("/summary/{lang}", response_model=schemas.Post, tags=['summary'])
# Summary endpoint
async def summary(
    lang: str,
    post_data: schemas.PostCreate = Body(..., example=example_request),
    db: Session = Depends(get_db),
):
    if lang not in nlp:
        raise HTTPException(status_code=400, detail="Language not supported")

    nlp_model = nlp[lang]
    doc = nlp_model(post_data.post_body)

    # Create a summary for the text
    num_sentences_in_summary = 3  # Adjust this as needed
    summary_sentences = [sent.text for sent in doc.sents][:num_sentences_in_summary]
    summary_text = ' '.join(summary_sentences)

    # Create a Post record with the summary    
    post_data.api_result = summary_text

    # Create a Post record with the summary_text
    post = models.Post(**post_data.dict())

    # Save the Post record to the database
    crud.create_post(db, post)

    return post


# Get a specific post by ID
@app.get("/posts/{post_id}", response_model=schemas.Post, tags=['edit_post'])
async def read_post(post_id: int, db: Session = Depends(get_db)):
    post = crud.get_post(db, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

# Get a list of posts
@app.get("/posts/", response_model=List[schemas.Post], tags=['list_post'])
async def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
