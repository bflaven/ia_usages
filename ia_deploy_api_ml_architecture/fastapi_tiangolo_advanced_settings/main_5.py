#!/usr/bin/python
# -*- coding: utf-8 -*-

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
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_deploy_api_ml_architecture/fastapi_tiangolo_advanced_settings/

# LAUNCH THE API
uvicorn main_5:app --reload

- requirements
pip install pydantic-settings
pip install python-dotenv


+ FastAPI Settings and Environment Variables
--- Source: https://fastapi.tiangolo.com/advanced/settings/

GET /greet
Headers:
lang: EN

GET /greet
Headers:
lang: SP


"""
from fastapi import FastAPI, Depends, Header

app = FastAPI()

# Define a dependency to get the language from the "lang" header.
def get_language(lang: str = Header(None)):
    # Here, we're getting the "lang" header, but you can customize this to read from different sources.
    # You can also implement language detection logic if needed.
    return lang

# Use the get_language dependency to set the language for the entire API session.
@app.get("/greet")
async def greet(name: str, lang: str = Depends(get_language)):
    if lang == "SP":
        return {"message": f"Hola, {name}!"}
    else:
        return {"message": f"Hello, {name}!"}




