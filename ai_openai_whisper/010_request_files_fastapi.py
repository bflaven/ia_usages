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
uvicorn 010_request_files_fastapi:api --reload

# get the docs
http://127.0.0.1:8000/docs/
http://127.0.0.1:8000/redoc


# requirements
pip install fastapi
pip install "fastapi[all]"

[Source]
Source: https://fastapi.tiangolo.com/tutorial/request-files/

pip install python-multipart
pip install python-multipart



"""

import multipart
import whisper
import uvicorn
from moviepy.editor import AudioFileClip, VideoFileClip
from starlette.responses import RedirectResponse
from typing import Annotated
from fastapi import FastAPI, File, UploadFile


title="FastAPI request-files"
version="1.0"


api = FastAPI(title=title, version=version)


@api.get("/")
def root():
    return RedirectResponse(url="/docs")

@api.post("/upload")
def upload(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}

# https://stackoverflow.com/questions/63048825/how-to-upload-file-using-fastapi


@api.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@api.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
