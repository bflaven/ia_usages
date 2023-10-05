#!/usr/bin/python
# -*- coding: utf-8 -*-
#

"""
[env]
# Conda Environment
conda create --name ner_service python=3.9.13
conda info --envs
source activate ner_service
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n ner_service

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements_ner_service.txt

# to install
pip install -r requirements_ner_service.txt

# [path]
cd /Users/brunoflaven/Documents/03_git/BlogArticlesExamples/fastapi_nlp_model/002_bamimoretomi_spacy_fastapi

# launch the script
python ntlk_attempt_1.py

# LAUNCH THE API
uvicorn nlp_api:app --reload
Check http://127.0.0.1:8000/docs

# EXPLICATIONS
In this example, we've created three endpoints: /summary/{lang}, /ner/{lang}, and /custom-ner/{lang}, where {lang} is the language code (e.g., "en" for English). Each endpoint loads the appropriate spaCy model for the specified language and processes the input text accordingly.

You'll need to replace the summarize_text and extract_custom_entities functions with your actual summarization and custom NER logic. Additionally, you can customize the response format as needed.



# NLP_API description
- Place multiple languages: FR, ES, EN, RU
- functions available on the API built with FastAPI
--- provide a summary function
--- provide a keyword extraction function
--- provide a "normal" NER function
--- provide a “custom” NER function

- requirements
pip install fastapi[all] spacy
pip install gTTS


# install stuff

python -m spacy download en_core_web_sm
python -m spacy download es_core_news_sm
python -m spacy download fr_core_news_sm
python -m spacy download de_core_news_sm
pip install nltk

python -m spacy download en_core_web_lg 

# command to validate the model
python -m spacy validate


# to load the models
nlp = spacy.load("en_core_web_sm")
nlp = spacy.load("en_core_web_lg")



"""



import nltk
from nltk.corpus import wordnet

synonyms = []
antonyms = []
  
for syn in wordnet.synsets("good"):
    for l in syn.lemmas():
        synonyms.append(l.name())
        if l.antonyms():
            antonyms.append(l.antonyms()[0].name())
  
print(set(synonyms))
print(set(antonyms))




