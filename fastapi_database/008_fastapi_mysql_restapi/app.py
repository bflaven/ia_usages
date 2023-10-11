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
cd /Users/brunoflaven/Documents/03_git/ia_usages/fastapi_database/008_fastapi_mysql_restapi/

# LAUNCH THE API
uvicorn app:app --reload

# Check localhost
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc

# check phpmyadmin
http://127.0.0.1:8080/
root:password

- requirement for sqlalchemy
pip install sqlalchemy

Source: https://github.com/FaztWeb/fastapi-mysql-restapi/tree/main

"""
from fastapi import FastAPI
from routes.user import user
from config.openapi import tags_metadata

app = FastAPI(
    title="Users API YT",
    description="a REST API using python and mysql",
    version="0.0.1",
    openapi_tags=tags_metadata,
)

app.include_router(user)
