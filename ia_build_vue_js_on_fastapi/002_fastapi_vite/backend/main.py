#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
[env]
# Conda Environment
conda create --name fmm_fastapi_poc python=3.9.13
conda info --envs
source activate fmm_fastapi_poc
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]

conda env remove -n fmm_fastapi_poc

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt


# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_build_vue_js_on_fastapi/002_fastapi_vite/backend


# LAUNCH THE API
uvicorn main:app --reload

# local
http://localhost:8000
http://127.0.0.1:8000


"""


# main.py

# for mamania
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
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
        'name': 'things',
        'description': 'List things just to have some json result.'
    },
    {
        'name': 'sentiment_analysis',
        'description': 'use to give a sentiment analysis for comment in French with the help of Camembert.'
    },
    {
        'name': 'namegenerator',
        'description': 'TRUE. Just type a lowercase letter, for example "m" and you will get a random name starting with "m" from the following names: "Bernard", "Jonas", "Nomonde", "Robert", " Guido", "Lorenzo", "Pia", "Prisca", "Minnie". ", "Margaret", "Myrtle", "Noa", "Nadia". This is the only endpoint working.'
    }
]

# API INFOS
API_TITLE = 'POC_1 MamamIA'
API_VERSION = '1.0'
HOME_API_NAME = 'V1.0 - MamamIA - Azure FastAPI POC API'
HOME_API_DESCRIPTION = 'Some endpoints for API made with FastAPI for basic deployment on Azure. One is with Sentiment analyis.'



# to get elements
class Item(BaseModel):
    id: int
    example: str

# Define request body model
class NameSearch(BaseModel):
    name_search: str


app = FastAPI(
    title=""+API_TITLE+"",
    description=""+HOME_API_NAME+" - "+HOME_API_DESCRIPTION+"",
    openapi_tags=tags_metadata,
    version=""+API_VERSION+"",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # You can specify specific origins instead of allowing all with "*"
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)



######################### API ENDPOINTS #################################

### CLASSICAL ENDPOINTS    
@app.get("/", include_in_schema=False)
async def home():
    # For direct redirection to docs swagger
    return RedirectResponse("/docs")
    # return {''+HOME_API_NAME+'':''+HOME_API_DESCRIPTION+''}

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

@app.get("/generate_name", tags=['namegenerator'])
async def generate_name(starts_with: str = None):
    
    # return {"starts_with": starts_with}
    names = ["Bernard", "Jonas", "Nomonde", "Robert", "Guido", "Lorenzo", "Pia", "Prisca", "Minnie", "Margaret", "Myrtle", "Noa", "Nadia"]
    if starts_with:
        names = [n for n in names if n.lower().startswith(starts_with)]
    random_name = random.choice(names)
    return {"name": random_name}




@app.get("/things", tags=['things'])
async def things() -> List[Item]:
    return [
        Item(id=1, example="example1"), 
        Item(id=2, example="example2"),
        Item(id=3, example="example3"),
        Item(id=4, example="example4"),
        Item(id=5, example="example5"),
        Item(id=6, example="example6"),
        Item(id=7, example="example7"),
        Item(id=8, example="example8")

        ]





    