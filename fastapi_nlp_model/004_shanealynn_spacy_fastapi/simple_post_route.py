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
uvicorn simple_post_route:app --reload



"""
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define the expected JSON format as a class from Pydantic:
class QueryString(BaseModel):
    """
    This class only contains one element, a string called "query".
    This setup will set Pydantic to expect a dictionary of format:
    {"query": "Some sort of string"}
    """
    query: str


# Add a simple GET response at the base url "/"
@app.get("/")
def read_root():
    return {"test_response": "Hello World!"}


# set up a route that is accessed with POST
@app.post("/analysis/")
def analyse_text(query_string: QueryString):
    return {
        "dataReceived": query_string,
        "yeah": True,
        }
