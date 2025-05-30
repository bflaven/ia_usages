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
python 002_controlling-large-language-model-output-with-pydantic.py


# source
https://medium.com/@mattchinnock/controlling-large-language-model-output-with-pydantic-74b2af5e79d1
"""


from pydantic.v1 import BaseModel, Field, Extra
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser
from pydantic.v1 import ValidationError


# Example tweets and their metadata
raw_tweets = [
    {"id": "001", "text": "It's been a week since the Sparks Valley fire roared to life, and it's now the largest wildfire in state history.", "date": "03-04-2024"},
    {"id": "002", "text": "Video of the flames destroying my neighborhood. **** that fire! #firessuck", "date": "03-04-2024"},
    {"id": "003", "text": "I blame Biden for the #sparksvalleyfire response", "date": "02-29-2024"},
]


class Tweet(BaseModel):
    isPolitical: bool = Field(description="Whether the tweet is political")
    isOffensive: bool = Field(description="Whether the tweet is offensive")

    class Config:
        extra = Extra.forbid  # Forbid extra fields not defined in the model
# Note: 
# This example uses Langchain as a basis for interacting with a 
# local Ollama model but conceptually applies to any LLM.

llm = Ollama(model="mistral:latest")

screened_tweets = []

parser = JsonOutputParser(pydantic_object=Tweet)

def check_tweet(tweet):
    # Extract tweet text
    tweet_text = tweet['text']
    print(tweet_text)

    # Define a prompt template for assessing tweet content
    # and include the formatting instructions 
    prompt = PromptTemplate(
        template="""Assess whether the tweet contains references to politicians or political parties. 
        Assess if the tweet contains offensive language. 
        
        {format_instructions}
        
        {tweet_text}

        Only respond in the correct format, do not include additional properties in the JSON.\n""",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )


    # Construct a Langchain Chain to connect the prompt template with the LLM and Pydantic parser
    chain = prompt | llm | parser
    result = chain.invoke({"tweet_text": tweet_text})
    
    print(result)
    print("------")
    
    #Validate the output using the Pydantic model
    try:
        tweet_result = Tweet(**result) 
        # If valid, approve or reject tweet based on LLM output
        if not tweet_result.isPolitical and not tweet_result.isOffensive:
            screened_tweets.append(tweet)
            print(f"Adding {tweet['id']} to screened tweets.")
        else:
            print(f"Rejecting {tweet['id']}.")
    except ValidationError as e:
        print("Data output validation error, trying again...")
        # Retry tweet screening if validation fails
        check_tweet(tweet)


for tweet in raw_tweets:
    check_tweet(tweet)
