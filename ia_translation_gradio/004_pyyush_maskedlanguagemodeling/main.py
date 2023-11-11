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
pip freeze > requirements_full.txt

# to install
pip install -r requirements.txt

# install gradio
pip install gradio
conda install -c conda-forge gradio



# go to path
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_translation_gradio/004_pyyush_maskedlanguagemodeling/

# launch the api
uvicorn main:app --reload



# launch the Gradio.py
python ui.py


conda install -c anaconda rich
pip install rich

# check
The demo pop in a browser on 
http://localhost:7860 
or 
http://127.0.0.1:7860


"""
import uvicorn
from typing import Dict
from fastapi import FastAPI, File, status, APIRouter, Query, Header
from fastapi.responses import RedirectResponse
from fastapi.responses import StreamingResponse
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from transformers import pipeline




# pre-load pipelines
xlm_roberta_base = pipeline('fill-mask', model='xlm-roberta-base')
xlm_roberta_large = pipeline('fill-mask', model='xlm-roberta-large')

class Request(BaseModel):
    text: str
    model: str
    
class Response(BaseModel):
    text: str
    model: str
    predictions: Dict

# tags_metadata
tags_metadata = [
    {
        'name': 'healthcheck',
        'description': 'It basically sends a GET request to the route & hopes to get a "200"'
    },
    {
        'name': 'models',
        'description': 'The list the models available e.g Roberta (xlm-roberta-base, xlm-roberta-large). Usecase found in Masked Language Modeling from https://github.com/pyyush/MLM'
    },
    {
        'name': 'predict',
        'description': 'Some explanations: Masked language modeling predicts a masked token in a sequence, and the model can attend to tokens bidirectionally. This means the model has full access to the tokens on the left and right. Masked language modeling is great for tasks that require a good contextual understanding of an entire sequence. BERT is an example of a masked language model. See https://huggingface.co/docs/transformers/main/en/tasks/masked_language_modeling'
    }
]


# declaring FastAPI instance
app = FastAPI(
    title="mIAou",
    description="""V1.0 - POC for API made with FastAPI for basic deployment on Azure with Roberta (xlm-roberta-base, xlm-roberta-large) for Masked language modeling.""",
    openapi_tags=tags_metadata,
    version="1.0",
    )


######################### API ENDPOINTS #################################
@app.get("/", include_in_schema=False)
async def home():
    return RedirectResponse("/docs")
    # return {'V1.0 - mIAou - Azure FastAPI POC API': 'It is running and update must be automatic'}


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

@app.get("/models", tags=['models'])
def list_models():
    return {"models": ["xlm-roberta-base", "xlm-roberta-large"]}
 
@app.post('/predict', response_model=Response, tags=['predict'])
def predict(request: Request) -> Response:
    preds = {}
    
    outputs = xlm_roberta_large(request.text) if request.model.endswith("large") else xlm_roberta_base(request.text)

    for output in outputs:
        preds[output["token_str"]] = output["score"] 

    return Response(
        text = request.text, 
        model = request.model, 
        predictions = preds
        )

