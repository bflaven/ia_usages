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
conda env remove -n chainlit_python
conda env remove -n ai_chatgpt_prompts

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# [path]
cd /Users/brunoflaven/Documents/03_git/BlogArticlesExamples/fastapi_nlp_model/003_juliensalinas_spacy_fastapi/

# launch the api
uvicorn app:api --reload



"""

import spacy
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

# en_core_web_lg = spacy.load("en_core_web_lg")
en_core_web_lg = spacy.load("en_core_web_sm")

api = FastAPI()
# api = FastAPI(root_path="/api/v1")

class Input(BaseModel):
    sentence: str

class Extraction(BaseModel):
    first_index: int
    last_index: int
    name: str
    content: str

class Output(BaseModel):
    extractions: List[Extraction]

@api.get('/')
async def home():
    return {"Yo man / Welcome here / Benvenidos aqui"}

# @api.get('/')
# async def index():
#     return {"message": "Hello Bruno"}

@api.post("/extractions", response_model=Output)

async def extractions(input: Input):

    document = en_core_web_lg(input.sentence)

    extractions = []
    for entity in document.ents:
      extraction = {}
      extraction["first_index"] = entity.start_char
      extraction["last_index"] = entity.end_char
      extraction["name"] = entity.label_
      extraction["content"] = entity.text
      extractions.append(extraction)

    return {"extractions": extractions}


