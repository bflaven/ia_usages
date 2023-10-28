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
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_deploy_api_ml_architecture/mamamia-fastapi-azure/

# LAUNCH THE API
uvicorn app.main:app --reload

# get the docs
http://localhost:80


[Source]
Source: https://blog.pamelafox.org/2023/03/deploying-containerized-fastapi-app-to.html

"""

import random
from fastapi import FastAPI, File, status, APIRouter, Query, Header
from fastapi.responses import RedirectResponse
from fastapi.responses import StreamingResponse
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
from typing import Optional

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
        'name': 'advanced_summary',
        'description': 'For the moment, a fake endpoint. It waits for the function and the logic but it should enable to make a advanced_summary from a text.'
    },
    {
        'name': 'keywords',
        'description': 'For the moment, a fake endpoint. It waits for the function and the logic but it should enable to extract keywords from a text.'
    },
    {
        'name': 'transcription',
        'description': 'For the moment, a fake endpoint. It waits for the function and the logic but it should enable to extract a transcription from a audio file.'
    },
    {
        'name': 'namegenerator',
        'description': 'It generate random name....'
    }
]

app = FastAPI(
    title="MamamIA",
    description="""V2.5 - Many fake endpoints for API made with FastAPI for basic deployment on Azure.""",
    openapi_tags=tags_metadata,
    version="2.5",
)


######################### API ENDPOINTS #################################
@app.get("/", include_in_schema=False)
async def home():
    # return RedirectResponse("/docs")
    return {'V2.5 - MamamIA - Azure FastAPI POC API': 'It is running and update must be automatic'}

@app.get('/healthcheck', status_code=status.HTTP_200_OK, tags=['healthcheck'])
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


@app.get("/summary/", tags=['summary'])
async def get_summary():
    return {"summary": "fake endpoint that call function summary come here"}

# Function to perform NLP features with Spacy
@app.get("/nlp/advanced_summary" , tags=['advanced_summary'])
async def get_summary(language: str = Query(...), brand: str = Query(...), version: str = Query(...)):
    # Implement your summary extraction logic with Spacy here
    return {"message": "Advanced NLP Summary", "language": language, "brand": brand, "version": version}
# async def get_summary():
#     # Implement your summary extraction logic with Spacy here
#     return {"message": "fake endpoint - Advanced NLP Summary"}

@app.get("/nlp/keywords", tags=['keywords'])
async def get_keywords():
    # Implement your keyword extraction logic with Spacy here
    return {"message": "fake endpoint - NLP Keywords"}

@app.get("/nlp/entities", tags=['entities'])
async def get_entities():
    # Implement your entity extraction logic with Spacy here
    return {"message": "fake endpoint - NLP Entities"}

# Function to perform audio transcription with Whisper
@app.get("/audio/transcription", tags=['transcription'])
async def audio_transcription():
    # Implement audio transcription using Whisper here
    return {"message": "fake endpoint - Audio Transcription"}


@app.get("/generate_name", tags=['namegenerator'])
async def generate_name(starts_with: str = None):
    names = ["Bruno", "Anne", "Louise", "Robert", "Guido", "Lorenzo", "Pia", "Prisca", "Minnie", "Margaret", "Myrtle", "Noa", "Nadia"]
    if starts_with:
        names = [n for n in names if n.lower().startswith(starts_with)]
    random_name = random.choice(names)
    return {"name": random_name}


    