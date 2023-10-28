#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
conda create --name azure_fastapi python=3.9.13
conda info --envs
source activate azure_fastapi
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n azure_fastapi

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_deploy_api_ml_architecture/api_fastapi_routes/case_2_chatgpt_api_fastapi_routes/


# LAUNCH THE API
uvicorn app.main:app --reload

# Check localhost
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc


- requirements
pip install fastapi uvicorn
pip install spacy  # For NLP features
pip install scikit-learn  # For post-editorial category prediction

Here is some example of values: 
Language can have values like "es","fr","en", "ru"
Brand can have values like "rfi","f24","mcd", "obs"
API Version can have values like "v1","v2","v3"


"""
from fastapi import FastAPI, APIRouter, Query, Header
from typing import Optional

app = FastAPI(
	title="TrattorIA",
    description="""EXAMPLE_2 Routes examples for FastAPI""",
    version="2.0",
    )

# Create an APIRouter for your ML endpoints
ml_router = APIRouter()

# Define global parameters
global_language = None
global_brand = None
global_api_version = None

# Function to set up global parameters
@ml_router.on_event("startup")
async def setup_global_parameters():
    global global_language, global_brand, global_api_version
    # You can set these values based on your requirements, such as from request headers
    global_language = "en"
    global_brand = "rfi"
    global_api_version = "v1"

# Function to perform NLP features with Spacy
@ml_router.get("/nlp/summary")
async def get_summary():
    # Use global_language, global_brand, and global_api_version as needed
    return {"message": "NLP Summary", "language": global_language, "brand": global_brand, "version": global_api_version}


# Function to perform NLP features with Spacy
@ml_router.get("/nlp/advanced_summary")
async def get_summary(language: str = Query(...), brand: str = Query(...), version: str = Query(...)):
    # Implement your summary extraction logic with Spacy here
    return {"message": "Advanced NLP Summary", "language": language, "brand": brand, "version": version}

@ml_router.get("/nlp/keywords")
async def get_keywords(language: str = Query(...), brand: str = Query(...), version: str = Query(...)):
    # Implement your keyword extraction logic with Spacy here
    return {"message": "NLP Keywords", "language": language, "brand": brand, "version": version}

@ml_router.get("/nlp/entities")
async def get_entities(language: str = Query(...), brand: str = Query(...), version: str = Query(...)):
    # Implement your entity extraction logic with Spacy here
    return {"message": "NLP Entities"}

# Function to perform audio transcription with Whisper
@ml_router.get("/audio/transcription")
async def audio_transcription(language: str = Query(...), brand: str = Query(...), version: str = Query(...)):
    # Implement audio transcription using Whisper here
    return {"message": "Audio Transcription"}

# Function to perform video transcription with Whisper
@ml_router.get("/video/transcription")
async def video_transcription(language: str = Query(...), brand: str = Query(...), version: str = Query(...)):
    # Implement video transcription using Whisper here
    return {"message": "Video Transcription"}

# Function to predict post-editorial category with scikit-learn
@ml_router.get("/post_editorial/category")
async def post_editorial_category(language: str = Query(...), brand: str = Query(...), version: str = Query(...), text: str = Query(...)):
    # Implement post-editorial category prediction using scikit-learn here
    # You can pass 'text' in the query parameters to get the category prediction
    return {"category": "Predicted Category"}

# Mount the ML router with global parameters
app.include_router(ml_router, prefix="/ml")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



