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
python -m pip install python-dotenv



# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/_using_mlflow/djliden_usecase/

# launch the file
python 001_using_mlflow_djliden_usecase.py


# source_1
https://github.com/djliden/llmops-examples/tree/main
https://medium.com/@dliden/comparing-llms-with-mlflow-1c69553718df
https://mlflow.org/docs/latest/llms/langchain/guide/index.html
https://mlflow.org/docs/latest/llms/llm-evaluate/notebooks/huggingface-evaluation.html

# source_2
https://github.com/djliden/llmops-examples/blob/main/mlflow-compare-llms.ipynb


"""

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
# MOSAIC_API_KEY = os.environ["MOSAIC_API_KEY"]

#!mlflow gateway start --config-path config.yaml --port 5000 --host localhost --workers 2
#!mlflow deployments start-server --config-path config.yaml 

#!mlflow deployments start-server --config-path config.yaml --port 5000 --host localhost --workers 2


# let's run that as a subprocess
# cmd = ["mlflow", "gateway", "start", "--config-path", "config.yaml", "--port", "5000", "--host", "localhost", "--workers", "2"]
# process = subprocess.Popen(cmd)


# uncomment and run if you need to terminate the process
#process.terminate()

# gateway_client = MlflowGatewayClient("http://localhost:5000")
# gateway_client.search_routes()


# test the openai route
# response = gateway_client.query(
#     "chat_openai", {"messages": [{"role": "user", "content": "Tell me a joke about rabbits"}]}
# )
# print(response)





