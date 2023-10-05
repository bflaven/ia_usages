#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
CAUTION: RUN THE FILE database.py FIRST

[env]
# Conda Environment
conda create --name ner_spacy_fastapi_database python=3.9.13
conda info --envs
source activate ner_spacy_fastapi_database
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n ner_spacy_fastapi_database

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/fastapi_database/003_bugbytes_io_crud_api_fastapi_sqlmodel/

# LAUNCH THE API
uvicorn main:app --reload

# Check localhost
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc

- requirement
pip install sqlmodel

Source: https://bugbytes.io/posts/creating-a-music-track-api-with-fastapi-in-python/

"""
import json
import pathlib
from typing import List, Union

from fastapi import FastAPI, Response
from sqlmodel import Session, select

from models import Track
from database import TrackModel, engine

# instantiate the FastAPI app
app = FastAPI()


# define app start-up event
@app.on_event("startup")
async def startup_event():
    DATAFILE = pathlib.Path() / 'data' / 'tracks.json'

    # create a Session scoped to the startup event
    # Note: we can also use a context manager
    session = Session(engine)

    # check if the database is already populated
    stmt = select(TrackModel)
    result = session.exec(stmt).first()

    # Load data if there's no results
    if result is None:
        with open(DATAFILE, 'r') as f:
            tracks = json.load(f)
            for track in tracks:
                session.add(TrackModel(**track))
    
        session.commit()
    session.close()


@app.get('/')
def home():
    return {"Welcome here"}


@app.get('/tracks/', response_model=List[Track])
def tracks():
    return data
# http://localhost:8000/tracks/


@app.get('/tracks/{track_id}/', response_model=Union[Track, str])
def track(track_id: int, response: Response):
    # find the track with the given ID, or None if it does not exist
    track = next(
        (track for track in data if track["id"] == track_id), None
    )
    if track is None:
        # if a track with given ID doesn't exist, set 404 code and return string
        response.status_code = 404
        return "Track not found"
    return track

# curl -X 'GET' 'http://localhost:8000/tracks/' -H 'accept: application/json'
# http://localhost:8000/tracks/2/

@app.post("/tracks/", response_model=Track, status_code=201)
def create_track(track: Track):
    track_dict = track.dict()
    
    # assign track next sequential ID
    track_dict['id'] = max(data, key=lambda x: x['id']).get('id') + 1
    
    # append the track to our data and return 201 response with created resource
    data.append(track_dict)
    return track_dict

# curl -X POST -H "Content-Type: application/json" -d '{"artist": "Sonic Youth", "title": "Silver Rocket", "last_play": "2017-10-18 15:15:26", "duration": 200}' http://localhost:8000/tracks

@app.put("/tracks/{track_id}", response_model=Union[Track, str])
def update_track(track_id: int, updated_track: Track, response: Response):

    track = next(
        (track for track in data if track["id"] == track_id), None
    )

    if track is None:
        # if a track with given ID doesn't exist, set 404 code and return string
        response.status_code = 404
        return "Track not found"
    
    # update the track data
    for key, val in updated_track.dict().items():
        if key != 'id': # don't reset the ID
            track[key] = val
    return track

# curl -X PUT -H "Content-Type: application/json" -d '{"artist": "Sonic Youth", "title": "Silver Rocket", "last_play": "2017-10-18 15:15:26", "duration": 200}' http://localhost:8000/tracks/1


@app.delete("/tracks/{track_id}")
def delete_track(track_id: int, response: Response):

    # get the index of the track to delete
    delete_index = next(
        (idx for idx, track in enumerate(data) if track["id"] == track_id), None
    )

    if delete_index is None:
        # if a track with given ID doesn't exist, set 404 code and return string
        response.status_code = 404
        return "Track not found"
    
    # delete the track from the data, and return empty 200 response
    del data[delete_index]
    return Response(status_code=200)

# curl -X DELETE http://localhost:8000/tracks/1
