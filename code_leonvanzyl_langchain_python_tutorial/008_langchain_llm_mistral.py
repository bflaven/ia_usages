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
python 008_langchain_llm_mistral.py


https://python.langchain.com/docs/integrations/llms/ollama
https://www.youtube.com/watch?v=hVs8MVydN3A&list=PL4HikwTaYE0GEs7lvlYJQcvKhq0QZGRVn&index=2
https://github.com/leonvanzyl/langchain-python-tutorial/blob/lesson-1/llm.py


"""
# from langchain import StrOutputParser, Ollama, ChatPromptTemplate
# from langchain.prompts import ChatPromptTemplate

from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, CommaSeparatedListOutputParser




# disable for the moment deprecated message
import warnings
warnings.filterwarnings("ignore", category=UserWarning)


def call_string_output_parser():     
    llm_model = "mistral:latest"
    llm = Ollama(model=llm_model)
    parser = CommaSeparatedListOutputParser()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Generate a list of ten synonyms for the following word. Return the result as a comma separated list."),
        ("human", "{synonyms}")
    ])
    chain = prompt | llm | parser
    result = chain.invoke({"synonyms": "happy"})
    # Convert the result into a list
    return [result] 

print('\n–-- RESULT')
print(call_string_output_parser())

ze_type = type(call_string_output_parser())
print(ze_type)

