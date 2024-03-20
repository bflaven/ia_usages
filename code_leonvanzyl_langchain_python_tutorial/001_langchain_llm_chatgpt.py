#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
conda create --name langchain_fastapi_poc python=3.9.13
conda info --envs
source activate langchain_fastapi_poc
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n langchain_fastapi_poc

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

python -m pip install python-dotenv
python -m pip install langchain-openai

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_using_flowiseai/

# LAUNCH the file
python 001_langchain_llm_chatgpt.py



"""

from dotenv import load_dotenv
# Load environment variables from .env file

load_dotenv()

# Get API key from environment variable
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
)

response = llm.stream("Write a poem about AI")
# print(response)

for chunk in response:
    print(chunk.content, end="", flush=True)

