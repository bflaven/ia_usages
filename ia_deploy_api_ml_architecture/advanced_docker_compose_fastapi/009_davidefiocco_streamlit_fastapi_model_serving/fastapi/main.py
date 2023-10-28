#!/usr/bin/python
# -*- coding: utf-8 -*-
#

"""
[env]
# Conda Environment
conda create --name azure_fastapi python=3.9.13
conda info --envs
source activate azure_fastapi
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n azure_fastapi

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_deploy_api_ml_architecture/advanced_docker_compose_fastapi/009_davidefiocco_streamlit_fastapi_model_serving/


# LAUNCH THE API
uvicorn main:app --reload 

# get the docs
http://localhost:80/generate_name
http://localhost:8000/

[Source]
Source: https://blog.pamelafox.org/2023/03/deploying-containerized-fastapi-app-to.html

"""

import random
import fastapi

# tags_metadata
tags_metadata = [
    {
        'name': 'healthcheck',
        'description': 'It basically sends a GET request to the route & hopes to get a "200"'
    },
    {
        'name': 'summary',
        'description': 'For the moment, a fake endpoint. It waits for the function and the summarization logic but it should enable to make a summary from a text.'
    },
    {
        'name': 'namegenerator',
        'description': 'It generate random name....'
    }
]

app = fastapi.FastAPI(
    title="MamamIA",
    description="""Fake API made with FastAPI for basic deployment on Azure.""",
    openapi_tags=tags_metadata,
    version="1.0",
)


######################### API ENDPOINTS #################################
@app.get("/", include_in_schema=False)
async def home():
    return {'azure fastapi test api': 'It is running'}

@app.get("/summary/", tags=['summary'])
async def get_summary():
    return {"summary": "fake endpoint that call function summary come here"}

@app.get("/generate_name", tags=['namegenerator'])
async def generate_name(starts_with: str = None):
    names = ["Salomé", "Bruno", "Louise", "Prisca", "Minnie", "Margaret", "Myrtle", "Noa", "Nadia"]
    if starts_with:
        names = [n for n in names if n.lower().startswith(starts_with)]
    random_name = random.choice(names)
    return {"name": random_name}


    