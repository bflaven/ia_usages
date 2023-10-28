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
uvicorn main_4:app --reload

- requirements
pip install pydantic-settings
pip install python-dotenv


+ FastAPI Settings and Environment Variables
--- Source: https://fastapi.tiangolo.com/advanced/settings/


"""
from functools import lru_cache
from starlette.responses import RedirectResponse

from fastapi import Depends, FastAPI
from typing_extensions import Annotated

# import the config from config_4.py
import config_4

app = FastAPI(
    title="TrattorIA",
    description="""EXAMPLE_4 Using config for FastAPI""",
    version="1.0",
    )



@lru_cache()
def get_settings():
    return config_4.Settings()

@app.get('/', include_in_schema=False)
def home():
    # return {"nlp_db_app - Welcome here - Benvenidos aqui - Добро пожаловать - Bienvenue ici"}
    return RedirectResponse(f"/docs")

@app.get("/info")
async def info(settings: Annotated[config_4.Settings, Depends(get_settings)]):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }



