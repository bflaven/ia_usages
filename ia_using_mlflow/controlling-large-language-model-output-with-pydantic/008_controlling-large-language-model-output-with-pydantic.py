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
cd /Users/brunoflaven/Documents/01_work/blog_articles/_using_mlflow/controlling-large-language-model-output-with-pydantic/

# launch the file
python 008_controlling-large-language-model-output-with-pydantic.py


# source
https://medium.com/@mattchinnock/controlling-large-language-model-output-with-pydantic-74b2af5e79d1

https://www.learndatasci.com/solutions/how-to-use-open-source-llms-locally-for-free-ollama-python/



"""


from pydantic import BaseModel, Field, ValidationError
from typing import List

from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableSequence

# Define the CityResponse model using Pydantic for structured output
class CityResponse(BaseModel):
    city_name: str = Field(description="This is the Name of the city")
    country: str = Field(description="This is the country of the city")
    population_number: int = Field(description="This is the number of inhabitants")
    local_currency: str = Field(description="This is the local currency of the city")

# Define the Cities model, which contains a list of CityResponse objects
class Cities(BaseModel):
    city: List[CityResponse]

# Initialize the Ollama model with the desired model
llm = Ollama(model="mistral:latest")

# Define the Pydantic output parser to parse the response into the Cities model
pydantic_parser = PydanticOutputParser(pydantic_object=Cities)

# Define the query and the prompt template
query = "What are the top three big cities in Europe by population?"
prompt = PromptTemplate(
    template="Answer the user query in the following format:\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": pydantic_parser.get_format_instructions()},
)

# Construct the RunnableSequence with the prompt template, the LLM, and the output parser
chain = RunnableSequence([
    prompt,
    llm,
    pydantic_parser
])

# Run the chain with the query and parse the output into the Cities model
try:
    result = chain.invoke({"query": query})
    print(result)
except ValidationError as e:
    print("Validation error:", e)












