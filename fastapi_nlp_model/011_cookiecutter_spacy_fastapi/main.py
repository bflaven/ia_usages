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
conda env remove -n ner_service

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements_ner_service.txt

# to install
pip install -r requirements_ner_service.txt

# [path]
cd /Users/brunoflaven/Documents/03_git/BlogArticlesExamples/fastapi_nlp_model/011_cookiecutter_spacy_fastapi/

# LAUNCH THE API
uvicorn main:app --reload

# Check locahost
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc

"""
import uvicorn
from api import app


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080, log_level='info')