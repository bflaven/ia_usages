#!/usr/bin/python
# -*- coding: utf-8 -*-
#

"""
[env]
# Conda Environment
conda create --name open_interpreter python=3.9.13
conda info --envs
source activate open_interpreter
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n open_interpreter

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# [path]

cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_and_the_fake_prompt_academy
uvicorn 002_open_interpreter:app --reload

See https://docs.openinterpreter.com/setup#python-usage

- Installation
pip install open-interpreter


- Console or Terminal usage
interpreter


"""
# server.py

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from interpreter import interpreter

app = FastAPI()

@app.get("/chat")
def chat_endpoint(message: str):
    def event_stream():
        for result in interpreter.chat(message, stream=True):
            yield f"data: {result}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")

@app.get("/history")
def history_endpoint():
    return interpreter.messages



