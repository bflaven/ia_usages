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

# BURN AFTER READING
conda env remove -n using_mlflow


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# manual install
python -m pip install pdfx
python -m pip install pypdf
python -m pip install instructor



#required 
brew install poppler
brew install tesseract-lang 

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_testing_llm/

# launch the file
python 001_ia_testing_llm.py


[doc]
https://jxnl.github.io/instructor/examples/ollama/#ollama





"""
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List
import instructor



class Character(BaseModel):
    name: str
    age: int
    fact: List[str] = Field(..., description="A list of facts about the character")



# enables `response_model` in create call
client = instructor.from_openai(
    OpenAI(
        # http://127.0.0.1:11434
        base_url="http://localhost:11434/v1",
        api_key="ollama",  # required, but unused
    ),
    mode=instructor.Mode.JSON,

)

resp = client.chat.completions.create(
    # model="llama3",
    model="mistral:latest",
    messages=[
        {
            "role": "user",
            "content": "Tell 5 facts about Ludwig Wittgenstein?",
        }
    ],
    response_model=Character,
)
print(resp.model_dump_json(indent=2))



