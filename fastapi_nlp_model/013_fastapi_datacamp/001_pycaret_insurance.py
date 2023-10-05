#!/usr/bin/python
# -*- coding: utf-8 -*-
#
"""
[ENV]
# Conda Environment
conda create --name fastapi_datacamp
conda info --envs
source activate fastapi_datacamp
conda deactivate

# to export requirements
pip freeze > requirements_fastapi_datacamp.txt

# to install
pip install -r requirements_fastapi_datacamp.txt

# [path]
cd /Users/brunoflaven/Documents/03_git/BlogArticlesExamples/fastapi_nlp_model/013_fastapi_datacamp/



# launch the app
uvicorn main:app --reload
python pycaret_version.py

python 001_pycaret_insurance.py



# get the docs
http://127.0.0.1:8000/docs/
http://127.0.0.1:8000/redoc

# install

pip install typing
pip install fastapi
pip install pydantic
pip install uvicorn


pip install pycaret



"""


import pycaret
from pycaret.datasets import get_data
from pycaret.regression import *


# load the dataset
data = get_data('insurance')

s = setup(data, target = 'charges')

best = compare_models()

create_api (best, 'insurance_prediction_model')




