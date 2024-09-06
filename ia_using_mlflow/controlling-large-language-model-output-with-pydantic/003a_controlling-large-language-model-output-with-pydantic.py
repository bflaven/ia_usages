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
python -m pip install langchain-community langchain-core

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_using_mlflow/controlling-large-language-model-output-with-pydantic/

# launch the file
python 003a_controlling-large-language-model-output-with-pydantic.py


# source
https://medium.com/@mattchinnock/controlling-large-language-model-output-with-pydantic-74b2af5e79d1

https://www.learndatasci.com/solutions/how-to-use-open-source-llms-locally-for-free-ollama-python/



"""


from pydantic import BaseModel, Field
from typing import List

from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser
from pydantic.v1 import ValidationError

from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain.output_parsers import PydanticOutputParser

from langchain.prompts import PromptTemplate

# class CityResponse(BaseModel):
#     city_name: str = Field(description="This is the Name of the city")
#     country: str = Field(description="This is the country of the city")
#     population_number: int = Field(description="This is the number of inhabitants")
#     local_currency: str = Field(description="This is the local currency of the city")

# class Cities(BaseModel):
#     city: List[CityResponse]

class PostResponse(BaseModel):
    title: str = Field(description="This is the title of the post")
    summary: str = Field(description="This is the summary of the post")
    keywords: List[str] = Field(description="This is the 5 keywords of the post")
    categorie: str = Field(description="This is the categorie of the post")

# Define the Posts model, which contains a list of PostResponse objects
class Posts(BaseModel):
    post: List[PostResponse]



llm = Ollama(model="mistral:latest")

pydantic_parser = PydanticOutputParser(pydantic_object=Posts)
format_instructions = pydantic_parser.get_format_instructions()
print("-------------------------------------- format_instructions\n")
print(format_instructions)




# query = "What are the top three big cities in Europe by population?"
# prompt = PromptTemplate(
#     template="Answer the user query.\n{format_instructions}\n{query}\n",
#     input_variables=["query"],
#     partial_variables={"format_instructions": pydantic_parser.get_format_instructions()},
# )

# Construct a Langchain Chain to connect the prompt template with the LLM and Pydantic parser
# chain = prompt | llm | StrOutputParser






