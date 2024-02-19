#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
[env]
# Conda Environment
conda create --name sentiment_analysis python=3.9.13
conda info --envs
source activate sentiment_analysis
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt


# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_llms_usecases/fastapi_usecase_1_sentiment_analysis

[install]
# for ML
python -m pip install transformers
python -m pip install pyarrow
python -m pip install pandas
python -m pip install numpy
python -m pip install tensorflow
python -m pip install sentencepiece
python -m pip install torchvision 

# for API
python -m pip install fastapi uvicorn 
python -m pip install fastapi transformers

# for UX
python -m pip install streamlit requests

# LAUNCH THE API
uvicorn app.main:app --reload

# LAUNCH THE WEBAPP
streamlit run ux.py


# local
http://localhost:8000
http://127.0.0.1:8000

# docker
http://localhost
http://0.0.0.0:80


[source]
https://huggingface.co/cmarkea/distilcamembert-base-sentiment

The dataset comprises 204,993 reviews for training and 4,999 reviews for the test from Amazon, and 235,516 and 4,729 critics from Allocine website. The dataset is labeled into five categories:


1 étoile : représente une appréciation terrible,
2 étoiles : mauvaise appréciation,
3 étoiles : appréciation neutre,
4 étoiles : bonne appréciation,
5 étoiles : excellente appréciation.

1 star: represents a terrible appreciation,
2 stars: bad appreciation,
3 stars: neutral appreciation,
4 stars: good appreciation,
5 stars: excellent appreciation.

"""


# main.py

# for model
from .model import SentimentAnalysisModel

# for mamania
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import random
from fastapi import FastAPI, File, status, APIRouter, Query, Header
from fastapi.responses import RedirectResponse
from fastapi.responses import StreamingResponse
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
from typing import Optional


# tags_metadata
tags_metadata = [
    {
        'name': 'healthcheck',
        'description': 'TRUE. It basically sends a GET request to the route & hopes to get a "200"'
    },
    {
        'name': 'things',
        'description': 'TRUE. List things just to have some json result.'
    },
    {
        'name': 'sentiment_analysis',
        'description': 'TRUE. Use to give a sentiment analysis for comment in French with the help of Camembert.'
    },
    {
        'name': 'namegenerator',
        'description': 'TRUE. Just type a lowercase letter, for example "m" and you will get a random name starting with "m" from the following names: "Bernard", "Jonas", "Nomonde", "Robert", " Guido", "Lorenzo", "Pia", "Prisca", "Minnie". ", "Margaret", "Myrtle", "Noa", "Nadia". This is the only endpoint working.'
    }, {
        'name': 'summary',
        'description': 'FAKE. For the moment, a fake endpoint. It waits for the function and the summarization logic but it should enable to make a summary from a text.'
    },
    {
        'name': 'advanced_summary',
        'description': 'FAKE. For the moment, a fake endpoint. It waits for the function and the logic but it should enable to make a advanced_summary from a text. Required values for instance: language e.g.fr; brand e.g rfi; version e.g v1'
    },
    {
        'name': 'keywords',
        'description': 'FAKE. For the moment, a fake endpoint. It waits for the function and the logic but it should enable to extract keywords from a text.'
    },
    {
        'name': 'transcription',
        'description': 'FAKE. For the moment, a fake endpoint. It waits for the function and the logic but it should enable to extract a transcription from a audio file.'
    },
    {
        'name': 'entities',
        'description': 'FAKE. For the moment, a fake endpoint. It waits for the function and the logic but it should enable to extract a entities from a text (NER).'
    }
]

# API INFOS
API_TITLE = 'POC_1 MamamIA'
API_VERSION = '1.0'
HOME_API_NAME = 'V1.0 - MamamIA - Azure FastAPI POC API'
HOME_API_DESCRIPTION = 'Endpoints marked with TRUE are effective. The API is made with FastAPI for basic deployment on Azure.'



# to get elements
class Item(BaseModel):
    id: int
    example: str

# Define request body model
class NameSearch(BaseModel):
    name_search: str


app = FastAPI(
    title=""+API_TITLE+"",
    description=""+HOME_API_NAME+" - "+HOME_API_DESCRIPTION+"",
    openapi_tags=tags_metadata,
    version=""+API_VERSION+"",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # You can specify specific origins instead of allowing all with "*"
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


# Instantiate the SentimentAnalysisModel
sentiment_model = SentimentAnalysisModel()

######################### API ENDPOINTS #################################

### CLASSICAL ENDPOINTS    
@app.get("/", include_in_schema=False)
async def home():
    # For direct redirection to docs swagger
    return RedirectResponse("/docs")
    # return {''+HOME_API_NAME+'':''+HOME_API_DESCRIPTION+''}

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

@app.get("/generate_name", tags=['namegenerator'])
async def generate_name(starts_with: str = None):
    
    # return {"starts_with": starts_with}
    names = ["Bernard", "Jonas", "Nomonde", "Robert", "Guido", "Lorenzo", "Pia", "Prisca", "Minnie", "Margaret", "Myrtle", "Noa", "Nadia"]
    if starts_with:
        names = [n for n in names if n.lower().startswith(starts_with)]
    random_name = random.choice(names)
    return {"name": random_name}




@app.get("/things", tags=['things'])
async def things() -> List[Item]:
    return [
        Item(id=1, example="example1"), 
        Item(id=2, example="example2"),
        Item(id=3, example="example3"),
        Item(id=4, example="example4")
        ]


### FAKE ENDPOINTS ML OR IA  
@app.get("/summary/", tags=['summary'])
async def get_summary():
    return {"summary": "fake endpoint that call function summary come here"}

# Function to perform NLP features with Spacy
@app.get("/nlp/advanced_summary" , tags=['advanced_summary'])
async def get_summary(language: str = Query(...), brand: str = Query(...), version: str = Query(...)):
    # Implement your summary extraction logic with Spacy here
    return {"message": "Advanced NLP Summary", "language": language, "brand": brand, "version": version}
# async def get_summary():
#     # Implement your summary extraction logic with Spacy here
#     return {"message": "fake endpoint - Advanced NLP Summary"}

@app.get("/nlp/keywords", tags=['keywords'])
async def get_keywords():
    # Implement your keyword extraction logic with Spacy here
    return {"message": "fake endpoint - NLP Keywords"}

@app.get("/nlp/entities", tags=['entities'])
async def get_entities():
    # Implement your entity extraction logic with Spacy here
    return {"message": "fake endpoint - NLP Entities"}

# Function to perform audio transcription with Whisper
@app.get("/audio/transcription", tags=['transcription'])
async def audio_transcription():
    # Implement audio transcription using Whisper here
    return {"message": "fake endpoint - Audio Transcription"}



### ENDPOINTS ML    
@app.get("/sentiment-analysis/", tags=['sentiment_analysis'])
async def get_sentiment_analysis(message: str):
    """
    Perform sentiment analysis on the given message.
    """
    result = sentiment_model.analyze_sentiment(message)
    return result



    