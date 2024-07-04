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

# install manual
python -m pip install fastapi-utils
python -m pip install loguru


# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_build_vue_js_on_fastapi/006_fastapi_database/backend_2

# LAUNCH THE API
# be sure to be at he root dir cf [path]
uvicorn backend.main:app --reload

# local
http://localhost:8000
http://127.0.0.1:8000


"""


from backend import models, note
from fastapi import Depends, FastAPI, File, status, APIRouter, Query, Header, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.responses import StreamingResponse
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
from typing import Optional, List

# require to test in local
from fastapi.middleware.cors import CORSMiddleware

# db
from .database import engine
# debug
from loguru import logger

models.Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        'name': 'healthcheck',
        'description': 'It basically sends a GET request to the route & hopes to get a "200"'
    }
]
# API INFOS
API_TITLE = 'POV Aria'
API_VERSION = '1.0'
HOME_API_NAME = 'V1.0 - MamamIA - Azure FastAPI POC API'
HOME_API_DESCRIPTION = 'Many fake endpoints for API made with FastAPI for basic deployment on Azure. Only generate_name working.'


app = FastAPI(
    title=""+API_TITLE+"",
    description=""+HOME_API_NAME+" - "+HOME_API_DESCRIPTION+"",
    openapi_tags=tags_metadata,
    version=""+API_VERSION+"",
)

# Configure CORS
origins = [
    "http://localhost:3000",
    # Adjust this to the origin of your front-end app
    "http://127.0.0.1:5500",  
    # Add more origins if needed
    "http://localhost:5500",
    "http://127.0.0.1:8000",
    "http://localhost:8000",


    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(note.router, tags=['Notes'], prefix='/api/notes')


@app.get("/", include_in_schema=False)
async def home():
    # For direct redirection to docs swagger
    return RedirectResponse("/docs")
    # return {''+HOME_API_NAME+'':''+HOME_API_DESCRIPTION+''}


@app.get('/api/healthcheck', status_code=status.HTTP_200_OK, tags=['healthcheck'])
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


