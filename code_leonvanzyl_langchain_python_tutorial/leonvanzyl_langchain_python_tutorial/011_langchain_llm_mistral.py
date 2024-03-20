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
python 011_langchain_llm_mistral.py


https://python.langchain.com/docs/integrations/llms/ollama
https://www.youtube.com/watch?v=hVs8MVydN3A&list=PL4HikwTaYE0GEs7lvlYJQcvKhq0QZGRVn&index=2
https://github.com/leonvanzyl/langchain-python-tutorial/blob/lesson-1/llm.py

https://python.langchain.com/docs/get_started/introduction

- illustration
https://python.langchain.com/docs/modules/data_connection/

"""
# from langchain import StrOutputParser, Ollama, ChatPromptTemplate
# from langchain.prompts import ChatPromptTemplate

from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, CommaSeparatedListOutputParser, JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.documents import Document

# disable for the moment deprecated message
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Bruno Flaven has been a Project Manager in a wide variety of Internet (Mobile, Website) for 20 years now. Since 2023, Bruno Flaven is working mainly on AI.

docA = Document("Bruno Flaven has been a Project Manager in a wide variety of Internet (Mobile, Website) for 20 years now. Since 2023, Bruno Flaven is working mainly on AI.")


llm_model = "mistral:latest"
llm = Ollama(model=llm_model)

prompt = ChatPromptTemplate.from_template("""
Answer the user's question:
Question: {input}
Context: {context}
    """)
chain = prompt | llm
result = chain.invoke({
    "input": "Who is Bruno Flaven?",\
    "context": [docA]
    })

print('\n–-- RESULT')
print(result)

