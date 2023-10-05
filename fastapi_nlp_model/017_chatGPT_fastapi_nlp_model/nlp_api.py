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
cd /Users/brunoflaven/Documents/03_git/BlogArticlesExamples/fastapi_nlp_model/017_chatGPT_fastapi_nlp_model/

# LAUNCH THE API
uvicorn nlp_api:app --reload

python -m pytest

# Check localhost
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc

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

- requirements for fastapi
pip install fastapi
pip install spacy


- requirements for Spacy
python -m spacy download en_core_web_lg
python -m spacy download en_core_web_sm
python -m spacy download es_core_news_sm
python -m spacy download fr_core_news_sm
python -m spacy download ru_core_news_sm

# check install
python -m spacy validate

- requirements for audio (tospeech)
pip install gTTS


"""
####################################### IMPORT #################################

# json
import json

# other
from pydantic import BaseModel
from utils import *

# fastapi
from fastapi import FastAPI, File, status
from fastapi.responses import RedirectResponse
from fastapi.responses import StreamingResponse
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException

# spacy
import spacy

# tags_metadata
tags_metadata = [{
        'name': 'similarity',
        'description': 'Finds the similarity between 2 sentences using their word vectors.'
    },
    {
        'name': 'tokenize',
        'description': 'Takes in word, sentences e.t.c and return lexical infromation about each of words. e.g Nouns, Abstract Nouns, Co-ordinating conjunction.'
    },
    {
        'name': 'synonyms',
        'description': 'Takes in a word or a group of words separated by commas and return a list of English language synonyms for the words.'
    },
    {
        'name': 'antonyms',
        'description': 'Takes in a word or a group of words separated by commas and return a list of English language antonyms for the words.'
    },
    {
        'name': 'tospeech',
        'description': 'Takes in a string and returns an audio file of the text.'
    },
    {
        'name': 'healthcheck',
        'description': 'It basically sends a GET request to the route & hopes to get a "200"'
    },
    {
        'name': 'summary',
        'description': 'For the moment, a fake endpoint. It waits for the function and the summarization logic but it should enable to make a summary from a text.'
    },
    {
        'name': 'ner',
        'description': 'Takes in a string and returns entities (NER). Named Entity Recognition is a standard NLP problem which involves spotting named entities (people, places, organizations etc.) from a chunk of text, and classifying them into a predefined set of categories.'
    },
    {
        'name': 'custom-ner',
        'description': 'For the moment, a fake endpoint. It waits for a custom NER. It can be made with Spacy on specific entities such as Drugs, Fashion Brands...etc. Whatever you want.'
    },
    {
        'name': 'keywords',
        'description': 'Takes in a string and returns the main tags of the text.'
    }
]



# title
app = FastAPI(
    title="TrattorIA",
    description="""Obtain different features in NLP from Spacy in FR, ES, EN, RU + other features using nltk (nlp) and gtts (audio). It returns json as result.""",
    openapi_tags=tags_metadata,
    version="1.0",
)


# Load spaCy models for different languages
nlp_en = spacy.load("en_core_web_sm")
nlp_es = spacy.load("es_core_news_sm")
nlp_fr = spacy.load("fr_core_news_sm")
nlp_ru = spacy.load("ru_core_news_sm")

# This function is needed if you want to allow client requests 
# from specific domains (specified in the origins argument) 
# to access resources from the FastAPI server, 
# and the client and server are hosted on different domains.
origins = [
    "http://localhost",
    "http://localhost:8008",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



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

# startup
# @app.get("/")
# def read_root():
#     return {"NLP FastAPI Example": "Extend languages if needed"}

@app.on_event("startup")
def save_openapi_json():
    '''This function is used to save the OpenAPI documentation 
    data of the FastAPI application to a JSON file. 
    The purpose of saving the OpenAPI documentation data is to have 
    a permanent and offline record of the API specification, 
    which can be used for documentation purposes or 
    to generate client libraries. It is not necessarily needed, 
    but can be helpful in certain scenarios.'''
    openapi_data = app.openapi()
    # Change "openapi.json" to desired filename
    with open("openapi_nlp_api.json", "w") as file:
        json.dump(openapi_data, file)

# redirect
@app.get("/", include_in_schema=False)
async def redirect():
    return RedirectResponse("/docs")

@app.get('/healthcheck', status_code=status.HTTP_200_OK, tags=['healthcheck'])
def perform_healthcheck():
    '''
    It basically sends a GET request to the route & hopes to get a "200"
    response code. Failing to return a 200 response code just enables
    the GitHub Actions to rollback to the last version the project was
    found in a "working condition". It acts as a last line of defense in case something goes south.
    Additionally, it also returns a JSON response in the form of:
    {
        'healtcheck': 'Everything OK!'
    }
    '''
    return {'healthcheck': 'Everything OK!'}

######################### Support Func #################################

# Summary endpoint
@app.get("/summary/{lang}", tags=['summary'])
async def get_summary(text: str, lang: str):
    nlp = get_nlp_model(lang)
    doc = nlp(text)
    summary = summarize_text(doc)
    return {"summary": summary}

# Normal NER endpoint
@app.get("/ner/{lang}", tags=['ner'])
async def get_ner(text: str, lang: str):
    nlp = get_nlp_model(lang)
    doc = nlp(text)
    entities = extract_entities(doc)
    return {"entities": entities}

# Custom NER endpoint
@app.get("/custom-ner/{lang}", tags=['custom-ner'])
async def get_custom_ner(text: str, lang: str):
    nlp = get_nlp_model(lang)
    doc = nlp(text)
    custom_entities = extract_custom_entities(doc)
    return {"custom_entities": custom_entities}

# Keywords endpoint
@app.get("/keywords/{lang}", tags=['keywords'])
async def get_keywords(text: str, lang: str):
    nlp = get_nlp_model(lang)
    doc = nlp(text)

    # Create a dictionary to store the frequency of each keyword
    keyword_freq = {}

    # Iterate through tokens and count keyword frequency
    for token in doc:
        # Filter out stopwords and punctuation
        if not token.is_stop and not token.is_punct:
            lemma = token.lemma_.lower()  # Convert to lowercase
            keyword_freq[lemma] = keyword_freq.get(lemma, 0) + 1

    # Sort keywords by frequency in descending order
    sorted_keywords = sorted(keyword_freq.items(), key=lambda x: x[1], reverse=True)

    # Extract the top 10 keywords (you can change this number)
    top_keywords = [keyword for keyword, freq in sorted_keywords[:10]]

    return {"keywords": top_keywords}

# Helper function to get the appropriate spaCy model
def get_nlp_model(lang):
    if lang == "en":
        return nlp_en
    elif lang == "es":
        return nlp_es
    elif lang == "fr":
        return nlp_fr
    elif lang == "ru":
        return nlp_ru
    else:
        raise HTTPException(status_code=400, detail="Language not supported")

# Helper function to summarize text (you can use your preferred summarization method)
def summarize_text(doc):
    # Replace this with your summarization logic
    return doc.text
    


# Helper function to extract standard NER entities
def extract_entities(doc):
    entities = []
    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "start": ent.start_char,
            "end": ent.end_char,
            "label": ent.label_
        })
    return entities

# Helper function to extract custom NER entities using spaCy's Matcher
def extract_custom_entities(doc):
    custom_entities = []
    # Replace this with your custom NER logic using spaCy's Matcher
    return custom_entities

# EXTRA FUNCTIONS
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
