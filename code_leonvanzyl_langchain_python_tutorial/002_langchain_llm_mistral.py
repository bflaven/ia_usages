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
python 002_langchain_llm_mistral.py


https://python.langchain.com/docs/integrations/llms/ollama
https://www.youtube.com/watch?v=hVs8MVydN3A&list=PL4HikwTaYE0GEs7lvlYJQcvKhq0QZGRVn&index=2
https://github.com/leonvanzyl/langchain-python-tutorial/blob/lesson-1/llm.py
https://github.com/QuivrHQ/quivr/blob/c95c35499f7260e03cf6bc2d81560f134f85d8bd/backend/modules/brain/integrations/GPT4/Brain.py#L32



"""
from langchain_community.llms import Ollama
# from langchain.prompts import ChatPromptTemplate
from langchain_core.prompts import ChatPromptTemplate

# disable for the moment deprecated message
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# V1
# llm_model="mistral:latest"
# llm = Ollama(model=llm_model)
# response = llm.invoke("Tell me a joke")
# response = llm.invoke("Tell 3 facts about Simon Bolivar?")
# print(response)

# V2
# response = llm.stream("Write a poem about AI")
# response = llm.stream("Tell me a joke")
# print(response)
# for chunk in response:
#     print(chunk, end="", flush=True)
#     

# MODEL
# prompt template
# first_prompt = ChatPromptTemplate.from_template(
#         "Act as a highly intelligent news chatbot and classify the given news text into one of the following categories only 1. France 2. Europe 3. Africa 4. America 5. Asia-Pacific 6. Middle East 7. Sports 8. Economy 9. Technology 10. Culture 11. Environment. Do not code. Return only one word answer with only the category name that the given news text belongs to. In the output, return the result in a field named \"category_predicted:\" and return the comment in the field \"category_decision:\" in a python Dictionary.\t News text: {news}?"
#     ) 


# # V3
# # model name
# llm_model = "mistral:latest"
# # instantiate model
# llm = Ollama(model=llm_model)
# prompt = ChatPromptTemplate.from_template("Tell me a joke about {subject}")
# # create a LLM chain
# chain = prompt | llm 
# # Providing a string instead of a dictionary
# # response = chain.invoke({"subject": "scientist"})  
# response = chain.invoke({"subject": "dog"})  
# # ouput
# print (response)

# https://github.com/microsoft/JARVIS/blob/fb836f4a8c71ddcfb9ccc3835e3433232e51b7aa/easytool/easytool/funcQA.py#L63
# chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])







