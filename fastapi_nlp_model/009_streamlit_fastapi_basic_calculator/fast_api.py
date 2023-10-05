#!/usr/bin/python
# -*- coding: utf-8 -*-
#

"""
[env]
# Conda Environment
conda create --name streamlit_fastapi python=3.9.13
conda info --envs
source activate streamlit_fastapi
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n streamlit_fastapi

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# [path]
cd /Users/brunoflaven/Documents/03_git/BlogArticlesExamples/fastapi_nlp_model/009_streamlit_fastapi_basic_calculator/

# LAUNCH THE API
uvicorn fast_api:app --reload

Check 
http://127.0.0.1:8000/docs

"""
from fastapi import FastAPI
from pydantic import BaseModel
from calculator import calculate

class User_input(BaseModel):
    operation : str
    x : float
    y : float

app = FastAPI()

@app.post("/calculate")
def operate(input:User_input):
    result = calculate(input.operation, input.x, input.y)
    return result