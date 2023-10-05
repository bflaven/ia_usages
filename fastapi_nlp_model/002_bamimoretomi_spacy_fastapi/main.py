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
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# [path]
cd /Users/brunoflaven/Documents/03_git/BlogArticlesExamples/fastapi_nlp_model/002_bamimoretomi_spacy_fastapi

# LAUNCH THE API
uvicorn main:app --reload

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



from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from utils import *

tags_metadata=[
    {
        'name':'similarity',
        'description':'Finds the similarity between 2 sentences using their word vectors.'
    },
    {
        'name':'tokenize',
        'description':'Takes in word, sentences e.t.c and return lexical infromation about each of words. e.g Nouns, Abstract Nouns, Co-ordinating conjunction.'
    },
    {
        'name':'synonyms',
        'description':'Takes in a word or a group of words separated by commas and return a list of English language synonyms for the words.'
    },
    {
        'name':'antonyms',
        'description':'Takes in a word or a group of words separated by commas and return a list of English language antonyms for the words.'
    },
    {
        'name':'tospeech',
        'description':'Takes in a string and returns an audio file of the text.'
    }
]

class SimilarityIn(BaseModel):
    text_1 : str
    text_2 : str

class SimilarityOut(BaseModel):
    score : float

class TokenizeIn(BaseModel):
    text : str

class SynonymIn(BaseModel):
    text : str

class AntonymsIn(BaseModel):
    text : str

class TextToSpeech(BaseModel):
    text : str
    language : Optional[str] = 'en'

# title
app = FastAPI(title='Tageit',
              description='This is a hobby project for people interesed in using NLP. Email tomibami2020@gmail.com for new functionality you want to be added.',
              openapi_tags=tags_metadata)

@app.get('/')
def home():
    return 'Welcome here / Bienvenidos aqui'

@app.post('/similarity' , response_model=SimilarityOut,tags=['similarity'])
def similarity(text : SimilarityIn):
    score = similarity_(text.text_1, text.text_2)
    return {'score':score}

@app.post('/tokenize', response_model=dict,tags=['tokenize'])
def tokenize(text : TokenizeIn):
    tokens = tokenize_(text.text)
    return tokens

@app.post('/synonyms', response_model=dict, tags=['synonyms'])
def synonyms(text : SynonymIn ):
    words = text.text.replace(' ','').split(',')
    response = {}
    for i in words:
        syns = synonyms_(i.strip())
        response[i]=syns
        
    return response

@app.post('/antonyms', response_model=dict, tags=['antonyms'])
def antonyms(text : AntonymsIn ):
    words = text.text.replace(' ','').split(',')
    response = {}
    for i in words:
        syns = antonyms_(i.strip())
        response[i]=syns       
    return response

@app.post('/tospeech' ,tags=['tospeech'])
async def  text_to_speech(text : TextToSpeech ):
    language = text.language
    if len(language)>2:
        language=language[:2].lower()
    elif len(language)<2:
        language='en'
    audio_object = text_to_speech_(text.text,language=language)
    audio_object.save('aud.mp3')
    return FileResponse('aud.mp3')

