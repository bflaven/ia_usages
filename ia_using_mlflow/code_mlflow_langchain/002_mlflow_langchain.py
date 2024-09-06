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
python 002_mlflow_langchain.py


# source
https://github.com/manuelgilm/mlflow_for_ml_dev/tree/mlflow_for_ml_dev_legacy

"""

# for api key
import os
from dotenv import load_dotenv


from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Milvus

from langchain_core.output_parsers import StrOutputParser
from langchain_community.callbacks import get_openai_callback

from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain


### 1. GET API KEY ###
# Load environment variables from the .env file
load_dotenv()

# Access the API key using os.getenv
api_key = os.getenv("OPENAI_API_KEY")


llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.3,
        api_key=api_key,
        # openai_organization=OPENAI_ID_ORGANIZATION,
    )
chat_template = ChatPromptTemplate.from_messages(
        [
            ("user",
             """

             Who is {person} ?
             
             """
             ),
        ]
    )



chain = chat_template | llm | {"resposta": StrOutputParser()}

response = chain.invoke({"pergunta": query})
print response

