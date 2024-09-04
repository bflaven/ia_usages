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
python 005_controlling-large-language-model-output-with-pydantic.py


# source
https://medium.com/@mattchinnock/controlling-large-language-model-output-with-pydantic-74b2af5e79d1

https://www.learndatasci.com/solutions/how-to-use-open-source-llms-locally-for-free-ollama-python/
https://python.langchain.com/v0.1/docs/modules/model_io/output_parsers/quick_start/


"""


from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
# from langchain_openai import OpenAI
from langchain_community.llms import Ollama

# model = OpenAI(model_name="gpt-3.5-turbo-instruct", temperature=0.0)

# Initialize the Ollama model with the desired model
model = Ollama(model="mistral:latest")

# Define your desired data structure.
class Joke(BaseModel):
    setup: str = Field(description="question to set up a joke")
    punchline: str = Field(description="answer to resolve the joke")

    # You can add custom validation logic easily with Pydantic.
    @validator("setup")
    def question_ends_with_question_mark(cls, field):
        if field[-1] != "?":
            raise ValueError("Badly formed question!")
        return field


# Set up a parser + inject instructions into the prompt template.
parser = PydanticOutputParser(pydantic_object=Joke)

prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

# And a query intended to prompt a language model to populate the data structure.
prompt_and_model = prompt | model
output = prompt_and_model.invoke({"query": "Tell me a joke."})
# output = prompt_and_model.invoke({"query": "Tell me a joke?"})

print(output)
parser.invoke(output)


# Joke(setup='Why did the chicken cross the road?', punchline='To get to the other side!')










