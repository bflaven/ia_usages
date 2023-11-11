#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda ia_translation_facebook_nllb
conda create --name ia_translation_facebook_nllb python=3.9.13
conda info --envs
source activate ia_translation_facebook_nllb
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n ia_translation_facebook_nllb

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_translation/001a_giladd123_nllb_fastapi/

# case_1
uvicorn webserver:app --reload

# get the docs
http://127.0.0.1:8000/docs

# required
pip install srsly

"""
from fastapi import FastAPI, File, status, APIRouter, Query, Header
from translator import translator
import uvicorn
import json
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
# add some elements from fastapi
from fastapi.responses import RedirectResponse
from fastapi.responses import StreamingResponse
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
from typing import Optional
import srsly

# tags_metadata
tags_metadata = [
    {
        'name': 'healthcheck',
        'description': 'It basically sends a GET request to the route & hopes to get a "200"'
    },
    {
        'name': 'translate',
        'description': 'Text to present translation with nllb-200-distilled-600M'
    },
    {
        'name': 'languages',
        'description': 'Text to present languages for nllb-200-distilled-600M'
    }
]


app = FastAPI(
    title="TrattorIA",
    description="""V1.0 - Many fake endpoints for API made with FastAPI for basic deployment on Azure.""",
    openapi_tags=tags_metadata,
    version="1.0",
)
# translator = translator(model_dir, tokenizer_dir)
translator = translator ()

### DATA MODEL ###
class Request(BaseModel):
    src_lang: str
    tgt_lang: str
    input_text: str


class Error:
    error: str

    def __init__(self, error):
        self.error = error

### API ###
@app.get("/", include_in_schema=False)
async def home():
    return RedirectResponse("/docs")
    # return {'V1.0 - TrattorIA - Azure FastAPI POC API': 'It is up and running...'}

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
# Request = Body(..., example=example_request)
@app.post("/translate", tags=['translate'])
async def translate(request: Request ):
    invalid_languages = translator.validate_inputs(request.src_lang, request.tgt_lang)
    if len(invalid_languages) > 0:
        error = Error(
            f"Invalid language{'s' if len(invalid_languages) > 1 else '' }: {invalid_languages}, check /languages for a list of valid inputs"
        )
        return JSONResponse(content=jsonable_encoder(error), status_code=400)

    if not translator.check_langs_not_equal(request.src_lang, request.tgt_lang):
        error = Error("Source and target languages must not be the same")
        return JSONResponse(content=jsonable_encoder(error), status_code=400)

    result = translator.translate(**request.__dict__)

    result_json = {
        **request.__dict__,
        "output_text": result,
    }

    return JSONResponse(content=jsonable_encoder(result_json))


@app.get("/languages", tags=['languages'])
async def langs():
    content = {"languages": translator.lang_list}
    return JSONResponse(content=jsonable_encoder(content))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
