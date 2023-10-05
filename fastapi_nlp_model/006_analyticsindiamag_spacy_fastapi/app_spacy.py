#!/usr/bin/python
# -*- coding: utf-8 -*-
#

"""
[env]
# Conda Environment
conda create --name tagging_entity_extraction python=3.9.13
conda info --envs
source activate custom_spacy_ner_fastapi
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n chainlit_python
conda env remove -n ai_chatgpt_prompts

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > custom_spacy_ner_fastapi.txt

# to install
pip install -r custom_spacy_ner_fastapi.txt

# [path]
cd /Users/brunoflaven/Documents/03_git/BlogArticlesExamples/fastapi_nlp_model/006_analyticsindiamag_spacy_fastapi/

# LAUNCH THE API
uvicorn app_spacy:api --reload

Check http://127.0.0.1:8000/docs

"""

import spacy
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

en_core_web_sm = spacy.load("en_core_web_sm")

api = FastAPI()

class Input(BaseModel):
    sentence: str

class Extraction(BaseModel):
    first_index: int
    last_index: int
    name: str
    content: str

class Output(BaseModel):
    extractions: List[Extraction]

@api.post("/extractions", response_model=Output)
def extractions(input: Input):
    # document = en_core_web_lg(input.sentence)
    document = en_core_web_sm(input.sentence)

    extractions = []
    for entity in document.ents:
      extraction = {}
      extraction["first_index"] = entity.start_char
      extraction["last_index"] = entity.end_char
      extraction["name"] = entity.label_
      extraction["content"] = entity.text
      extractions.append(extraction)

    return {"extractions": extractions}

    