#!/usr/bin/python
# -*- coding: utf-8 -*-
#

"""
[env]
# Conda Environment
conda create --name ner_service python=3.9.13
conda info --envs
source activate ner_service
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n ner_service
conda env remove -n fastapi_datacamp

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements_ner_service.txt

# to install
pip install -r requirements_ner_service.txt

# [path]
cd /Users/brunoflaven/Documents/03_git/BlogArticlesExamples/fastapi_nlp_model/004_shanealynn_spacy_fastapi/

# LAUNCH THE API
uvicorn main:app --reload


"""
from pydantic import BaseModel
from fastapi import FastAPI
from get_entities_and_sentment import get_entities_and_sentiment


# MezzaVoce
app = FastAPI(
    title="MezzaVoce",
    description="""Obtain different features from Spacy in EN 
                    and return json result + sentiment analysis""",
    version="1.0",
)


class QueryString(BaseModel):
    query: str


@app.get("/")
def read_root():
    return {"test_response": "The API is working!"}


@app.post("/analysis/")
def analyse_text(query_string: QueryString):

    sentiment, entities = get_entities_and_sentiment(query_string.query)
    return {
        "query": query_string.query,
        "entities": entities,
        "sentiment": sentiment,
        }
