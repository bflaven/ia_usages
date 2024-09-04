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
python -m pip pip install 'mlflow[genai]'



# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/_using_mlflow/djliden_usecase/

# launch the file
python 003_using_mlflow_djliden_usecase.py


# source_1
https://github.com/djliden/llmops-examples/tree/main
https://medium.com/@dliden/comparing-llms-with-mlflow-1c69553718df
https://mlflow.org/docs/latest/llms/langchain/guide/index.html
https://mlflow.org/docs/latest/llms/llm-evaluate/notebooks/huggingface-evaluation.html

# source_2
https://github.com/djliden/llmops-examples/blob/main/mlflow-compare-llms.ipynb

# Evaluating LLMs with MLflow by Miloš Švaňa
https://www.youtube.com/watch?v=PoVDjwiUCJY&t=906s

"""

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# llm = Ollama(model="mistral:latest")
# print(llm("Who is Kamala Harris?"))

## Prompt Template

prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant. Please response to the user queries"),
        ("user","Question:{question}")
    ]
)


llm=Ollama(model="mistral:latest")
output_parser=StrOutputParser()
chain=prompt|llm|output_parser

input_text = "Who is Kamala Harris?"

print(chain.invoke({'question':input_text}))





