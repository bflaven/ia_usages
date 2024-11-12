#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
[env]
# Conda Environment
conda create --name ia_spacy_llm python=3.9.13
conda info --envs
source activate ia_spacy_llm
conda deactivate


# BURN AFTER READING
source activate ia_spacy_llm

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n ia_spacy_llm

# BURN AFTER READING
conda env remove -n ia_spacy_llm


# other libraries
python -m pip install spacy 
python -m pip install spacy-llm 
python -m pip install scikit-learn
python -m pip install python-dotenv
python -m pip install langchain-openai

# spacy
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_md
python -m spacy validate

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_spacy_llm/


# launch the file
python 001_ia_spacy_llm.py

# source
Source: https://realpython.com/natural-language-processing-spacy-python/

https://github.com/bflaven/BlogArticlesExamples/blob/3ffb3f7c17ccd5be0f988248a342b74f440232fb/extending_streamlit_usage/001_nlp_spacy_python_realp/005_nlp_spacy_python.py

"""

import spacy
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


# EN
nlp = spacy.load('en_core_web_sm')

# FR
# nlp = spacy.load('fr_core_news_sm')

print("\n --- result_1")
# EN
print("EN spacy loaded")

# FR
# print("FR spacy loaded")





# from spacy_llm import LLMWrapper
# from spacy.tokens import DocBin
# from sklearn.metrics import jaccard_score
# from sklearn.preprocessing import MultiLabelBinarizer

# nlp = spacy.blank("en")
# nlp.add_pipe("llm")
# doc = nlp("This is a blog post about NLP.")
# labels = ["news", "blog", "article"]
# prediction = nlp.predict(doc, labels)
# print(prediction)


