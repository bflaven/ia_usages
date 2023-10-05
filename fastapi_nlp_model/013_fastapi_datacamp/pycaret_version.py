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
cd /Users/brunoflaven/Documents/03_git/BlogArticlesExamples/fastapi_nlp_model/013_fastapi_datacamp/



# launch the app
uvicorn main:app --reload
python pycaret_version.py

# get the docs
http://127.0.0.1:8000/docs/
http://127.0.0.1:8000/redoc

# install

pip install typing
pip install fastapi
pip install pydantic


pip install pycaret



"""


import pycaret

print(f'pycaret version :: '+pycaret.__version__)




