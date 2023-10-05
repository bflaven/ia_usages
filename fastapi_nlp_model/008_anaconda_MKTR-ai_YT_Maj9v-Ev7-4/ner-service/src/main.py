#!/usr/bin/python
# -*- coding: utf-8 -*-
#
"""
[ENV_1]
# Using Poetry
See pyproject_good_full.toml

[ENV_2]
# Using Anaconda

# Conda Environment
conda create --name ner_service python=3.9.13
conda info --envs
source activate ner_service
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n ner_service

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements_ner-service.txt

# to install
pip install -r requirements_tagging_entity_extraction.txt

# [path]
cd /Users/brunoflaven/Documents/03_git/BlogArticlesExamples/fastapi_nlp_model/008_anaconda_MKTR-ai_YT_Maj9v-Ev7-4/ner-service/src


# LAUNCH THE API
uvicorn main:app --reload

# Check localhost
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc


# install spacy
pip install -U pip setuptools wheel
pip install -U spacy
python -m spacy download en_core_web_sm
python -m spacy download fr_core_news_sm



"""
from fastapi import FastAPI
from typing import List
import spacy
import spacy.cli

from models import Payload, Entities


app = FastAPI()

nlp = spacy.load("en_core_web_sm")
# nlp = spacy.load("fr_core_news_sm")


@app.get('/')
async def index():
    return {"message": "Hello Bruno"}

@app.post('/ner-service')
async def get_ner(payload: Payload):
    tokenize_content: List[spacy.tokens.doc.Doc] = [
        nlp(content.content) for content in payload.data
    ]
    document_enities = []
    for doc in tokenize_content:
        document_enities.append([ {'text': ent.text, 'entity_type': ent.label_} for ent in doc.ents ])
    return [
        Entities(post_url=post.post_url, entities=ents)
        for post, ents in zip(payload.data, document_enities)
    ]



    