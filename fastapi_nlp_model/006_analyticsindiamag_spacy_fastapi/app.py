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

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements_ner_service.txt

# to install
pip install -r requirements_ner_service.txt

# [path]
cd /Users/brunoflaven/Documents/03_git/BlogArticlesExamples/fastapi_nlp_model/017_chatGPT_fastapi_nlp_model/

# LAUNCH THE API
uvicorn app:api --reload

Check http://127.0.0.1:8000/docs

"""

from fastapi import FastAPI
api = FastAPI()
@api.get("/")
def index():
    return {"message": "Hello Bruno"}

