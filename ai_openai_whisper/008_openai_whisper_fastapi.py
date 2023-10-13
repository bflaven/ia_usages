#!/usr/bin/python
# -*- coding: utf-8 -*-
#

"""
[env]
# Conda Environment
conda create --name openai_whisper python=3.9.13
conda info --envs
source activate openai_whisper
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n openai_whisper

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_openai_whisper/

[Source]
Source: https://github.com/openai/whisper/tree/main
git clone https://github.com/openai/whisper.git

[MODELS AND LANGUAGES]
Available models and languages
There are five model sizes, four with English-only versions, offering speed and accuracy tradeoffs. Below are the names of the available models and their approximate memory requirements and relative speed.

tiny
base
small
medium
large

See https://github.com/openai/whisper/tree/main#available-models-and-languages


# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_openai_whisper/


# launch the app
uvicorn 008_openai_whisper_fastapi:api --reload

# get the docs
http://127.0.0.1:8000/docs/
http://127.0.0.1:8000/redoc


# requirements
pip install fastapi
pip install "fastapi[all]"

[Source]
Source: https://github.com/openai/whisper/tree/main
git clone https://github.com/openai/whisper.git



"""
import os
import whisper
import uvicorn
import multipart
from typing import Annotated
from fastapi import FastAPI, File, UploadFile
from moviepy.editor import AudioFileClip, VideoFileClip
from starlette.responses import RedirectResponse


title="FastAPI to access AI Whisper's features for audio and video transcription"
version="alpha.1.1"


# values for audio
# spanish
# audio_input = "audio_files_sources/foreign/sp_sample_1.mp3"
# file_output = "003_openai_whisper_sp_sample_1_output.txt"
# language_selected="spanish"



api = FastAPI(title=title, version=version)
    
@api.get("/", description="The root redirect to swagger user interface")
def root():
    return RedirectResponse(url="/docs")

# values for audio
audio_mp3 = "audio_files_sources/foreign/sp_sample_1.mp3"
host_dev = "127.0.0.1"
port_dev = "8888"

# values for documentation
title = "FastAPI to access AI Whisper's features for audio and video transcription"
version = "alpha.1.1"

api = FastAPI(title=title, version=version)


@api.get("/", description="The root redirect to swagger user interface")
def root():
    return RedirectResponse(url="/docs")


@api.post("/audio", description="This is the audio transcription")
async def audio(file: UploadFile = File()):
    if "audio" in file.content_type:
        audio_source = "audio_source." + file.filename[-3:]
        audio_content = await file.read()
        open(audio_source, "wb").write(audio_content)
        audio = AudioFileClip(audio_source)
        audio.write_audiofile(audio_mp3, codec="mp3")
        model = whisper.load_model("base")
        result = model.transcribe(audio_mp3, fp16=False)
        os.remove(audio_source)
        os.remove(audio_mp3)
        return result["text"]
    else:
        return "This file is not an audio file"


@api.post("/video", description="This is the video transcription")
async def video(file: UploadFile = File()):
    if "video" in file.content_type:
        video_source = "video_source." + file.filename[-3:]
        video_content = await file.read()
        open(video_source, "wb").write(video_content)
        video = VideoFileClip(video_source)
        audio = video.audio
        audio.write_audiofile(audio_mp3, codec="mp3")
        model = whisper.load_model("base")
        result = model.transcribe(audio_mp3, fp16=False)
        os.remove(video_source)
        os.remove(audio_mp3)
        return result["text"]
    else:
        return "This file is not an video file"

if __name__ == "__main__":
    if len(os.sys.argv) == 1:
        host = host_dev
        port = int(port_dev)
    elif len(os.sys.argv) == 2:
        host = os.sys.argv[1]
        port = int(port_dev)
    elif len(os.sys.argv) == 3:
        host = os.sys.argv[1]
        port = int(os.sys.argv[2])
    uvicorn.run("fastapi_whisper:api", host=host, port=port, reload=True)
