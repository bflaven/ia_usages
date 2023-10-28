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
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_deploy_api_ml_architecture/api_fastapi_routes/case_3_chatgpt_api_fastapi_routes/



# LAUNCH THE API
# V1
uvicorn app.main:app --reload 

# V2
LANGUAGE="en" BRAND="f24" API_VERSION="v1" uvicorn app.main:app --reload


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
from fastapi import FastAPI, APIRouter, Query
from typing import Optional
import os

language = os.environ.get("LANGUAGE")
brand = os.environ.get("BRAND")
api_version = os.environ.get("API_VERSION")

app = FastAPI(
    title="TrattorIA",
    description="""EXAMPLE_3 Routes examples for FastAPI. Check endpoints: summary & category""",
    version="2.0",
    )


# Define the APIRouter
router = APIRouter()

# Define the global parameters
@router.on_event("startup")
async def startup_event():
    app.state.language = language
    app.state.brand = brand
    app.state.api_version = api_version

    # DEBUG
    # print(f"language :: {language}")
    # print(f"brand :: {brand}")
    # print(f"api_version :: {api_version}")

# Function to set the global parameters using query parameters
@router.get("/set_parameters/")
async def set_parameters(
    language: str = Query(..., description="Language", regex=r"^(es|fr|en|ru)$"),
    brand: str = Query(..., description="Brand", regex=r"^(rfi|f24|mcd|obs)$"),
    version: str = Query(..., description="API Version", regex=r"^(v1|v2|v3)$"),
):
    app.state.language = language
    app.state.brand = brand
    app.state.api_version = version

    return {"message": "Global parameters set"}


# NLP features with Spacy
@router.get("/nlp/summary")
async def nlp_summary(
    text: str = Query(..., description="Text to summarize")

    ):
    # Use app.state.language, app.state.brand, and app.state.api_version here
    # Implement the Spacy summary logic
    return {"summary": "Your summarized text", "language": language, "brand": brand, "version": api_version}

# NLP features with Spacy
@router.get("/nlp/summary")
async def nlp_summary(text: str = Query(..., description="Text to summarize")):
    # Use app.state.language, app.state.brand, and app.state.api_version here
    # Implement the Spacy summary logic
    return {"summary": "Your summarized text"}

@router.get("/nlp/keywords")
async def nlp_keywords(text: str = Query(..., description="Text to extract keywords from")):
    # Use app.state.language, app.state.brand, and app.state.api_version here
    # Implement the Spacy keyword extraction logic
    return {"keywords": ["keyword1", "keyword2"]}

@router.get("/nlp/entities")
async def nlp_entities(text: str = Query(..., description="Text to extract entities from")):
    # Use app.state.language, app.state.brand, and app.state.api_version here
    # Implement the Spacy entity extraction logic
    return {"entities": ["entity1", "entity2"]}

# Audio transcription with Whisper
@router.get("/audio/transcription")
async def audio_transcription(audio_url: str = Query(..., description="Audio URL")):
    # Use app.state.language, app.state.brand, and app.state.api_version here
    # Implement Whisper audio transcription logic
    return {"transcription": "Your audio transcription"}

# Video transcription with Whisper
@router.get("/video/transcription")
async def video_transcription(video_url: str = Query(..., description="Video URL")):
    # Use app.state.language, app.state.brand, and app.state.api_version here
    # Implement Whisper video transcription logic
    return {"transcription": "Your video transcription"}

# Post editorial category prediction with scikit-learn
@router.get("/post/editorial_category")
async def predict_editorial_category(text: str = Query(..., description="Text to predict category for")):
    # Use app.state.language, app.state.brand, and app.state.api_version here
    # Implement the scikit-learn category prediction logic
    # Return the predicted category
    return { "category": "US", "language": language, "brand": brand, "version": api_version}

    

# Add the router to the FastAPI app
app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)





