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
python 005_langchain_llm_mistral.py


https://python.langchain.com/docs/integrations/llms/ollama
https://www.youtube.com/watch?v=hVs8MVydN3A&list=PL4HikwTaYE0GEs7lvlYJQcvKhq0QZGRVn&index=2
https://github.com/leonvanzyl/langchain-python-tutorial/blob/lesson-1/llm.py


"""
from langchain import StrOutputParser, Ollama, ChatPromptTemplate

# disable for the moment deprecated message
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

def call_string_output_parser():     
        llm_model = "mistral:latest"
        llm = Ollama(model=llm_model)
        # need to instantiate
        parser = StrOutputParser()
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Tell me a joke about the following subject"),
            ("human", "{subject}")
        ])
        chain = prompt | llm | parser
        return chain.invoke({"subject": "dog"})


print(call_string_output_parser())
