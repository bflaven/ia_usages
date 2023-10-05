#!/usr/bin/python
# -*- coding: utf-8 -*-
#
"""
[ENV_1]
# Conda Environment
conda create --name ner_service
conda info --envs
source activate ner_service
conda deactivate


# to export requirements
pip freeze > requirements_ner-service.txt

# to install
pip install -r requirements_ner-service.txt

# [path]
cd /Users/brunoflaven/Documents/03_git/BlogArticlesExamples/fastapi_nlp_model/012_fastapi_tiangolo_testing/app


# launch the app
uvicorn 001_fastapi_testing:app --reload

# lauch the test
python -m pytest




# install testing
pip install httpx
pip install starlette
pip install pytest

"""

from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Bienvenidos"}


