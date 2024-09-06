#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
conda create --name using_mlflow python=3.9.13
conda info --envs
source activate using_mlflow
conda deactivate

# BURN AFTER READING
source activate using_mlflow

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n using_mlflow
conda env remove -n locust_poc
conda env remove -n dam_step_process
conda env remove -n fmm_fastapi_poc

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# manual install
python -m pip install mlflow
python -m pip install starlette 
python -m pip install 'mlflow[genai]'
python -m pip install python-dotenv


# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_using_mlflow/djliden_usecase/

# launch the file
python 004_using_mlflow_djliden_usecase.py


# source_1
https://github.com/djliden/llmops-examples/tree/main
https://medium.com/@dliden/comparing-llms-with-mlflow-1c69553718df
https://mlflow.org/docs/latest/llms/langchain/guide/index.html
https://mlflow.org/docs/latest/llms/llm-evaluate/notebooks/huggingface-evaluation.html

# source_2
https://github.com/djliden/llmops-examples/blob/main/mlflow-compare-llms.ipynb

# Evaluating LLMs with MLflow by Miloš Švaňa
https://www.youtube.com/watch?v=PoVDjwiUCJY&t=906s

https://mlflow.org/docs/latest/llms/openai/notebooks/openai-quickstart.html



"""

import warnings

# Disable a few less-than-useful UserWarnings from setuptools and pydantic
warnings.filterwarnings("ignore", category=UserWarning)


import os

import openai
import pandas as pd
from IPython.display import HTML

import mlflow
from mlflow.models.signature import ModelSignature
from mlflow.types.schema import ColSpec, ParamSchema, ParamSpec, Schema

# for api key
import os
from dotenv import load_dotenv

# for ml flow
# import mlflow
# from mlflow.gateway import MlflowGatewayClient
# import subprocess


### 1. GET API KEY ###
# Load environment variables from the .env file
load_dotenv()

# Access the API key using os.getenv
# api_key = os.getenv("OPENAI_API_KEY")

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


# Run a quick validation that we have an entry for the OPEN_API_KEY within environment variables
assert "OPENAI_API_KEY" in os.environ, "OPENAI_API_KEY environment variable must be set"

# print(OPENAI_API_KEY)






