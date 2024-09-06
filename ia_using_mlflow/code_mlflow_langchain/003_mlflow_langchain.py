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



# BURN AFTER READING
conda env remove -n using_mlflow


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# manual install
pip install mlflow
python -m pip install mlflow
python -m pip install python-dotenv
python -m pip install openai


# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_using_mlflow/code_mlflow_langchain/

# launch the file
python 003_mlflow_langchain.py


# source
https://github.com/manuelgilm/mlflow_for_ml_dev/tree/mlflow_for_ml_dev_legacy

https://github.com/jersonortiz/llamachat/blob/main/simplechat.py


"""

# for api key
import time

from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm_model="mistral:latest"

llm = Ollama(model=llm_model)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are world class technical documentation writer."),
    ("user", "{input}")
])

output_parser = StrOutputParser()

chain = prompt | llm | output_parser

a = chain.invoke({"input": "how can langsmith help with testing?"})

while True:
    query = input('>>>')
    start = time.perf_counter()
    a = chain.invoke({"input": query})
    print(time.perf_counter() - start)
    print(a)







