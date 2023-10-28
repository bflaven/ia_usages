#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]

# create the env: fastapi_simple_app
python -m venv fastapi_simple_app
python -m venv env

# activate the env: fastapi_simple_app
source fastapi_simple_app/bin/activate
source env/bin/activate

# if you need to exit from the env fastapi_simple_app
deactivate

# If you need to update pip
pip install --upgrade pip
pip --version

# You can stay in the env  fastapi_simple_app or exit from this env to update pip

# install requirements
pip install fastapi
pip install uvicorn


# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_deploy_api_ml_architecture/fastapi-simple-app/

# launch the app
uvicorn app.main:api --reload


# Check localhost
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc



Source: https://getcodify.com/fastapi-a-simple-guide-with-installation-steps/

"""
	
# fastapi
from fastapi import FastAPI, File, status
# from fastapi.responses import RedirectResponse
# from fastapi.responses import StreamingResponse
# from fastapi.responses import FileResponse
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.exceptions import HTTPException

# tags_metadata
tags_metadata = [
    {
        'name': 'healthcheck',
        'description': 'It basically sends a GET request to the route & hopes to get a "200"'
    },
    {
        'name': 'summary',
        'description': 'For the moment, a fake endpoint. It waits for the function and the summarization logic but it should enable to make a summary from a text.'
    }
]
	
api = FastAPI(
    title="MamamIA",
    description="""Fake API made with FastAPI for basic deployment on Azure.""",
    openapi_tags=tags_metadata,
    version="1.0",
)

# home
@api.get("/", include_in_schema=False)
async def home():
    # return RedirectResponse("/docs")
    return {'fastapi test api': 'It is running'}

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

######################### Support Func #################################
@api.get("/summary/", tags=['summary'])
async def get_summary():
    return {"summary": "endpoint that call function summary come here"}


    