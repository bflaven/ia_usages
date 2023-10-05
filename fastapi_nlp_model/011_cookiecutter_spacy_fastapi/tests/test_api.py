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
cd /Users/brunoflaven/Documents/03_git/BlogArticlesExamples/fastapi_nlp_model/011_cookiecutter_spacy_fastapi/

# launch the test
pytest tests/test_api.py
python -m pytest --disable-warnings
pytest -q tests/test_api.py --disable-warnings

# [copyright]
Copyright (c) Microsoft Corporation. All rights reserved.
Licensed under the MIT License.

"""


import json
import pytest
# from PIL import Image
# import pandas as pd
import sys
import os
import io


from starlette.testclient import TestClient

# pytest app import fix
# dynamic_path = os.path.abspath('.')
# print(dynamic_path)
# sys.path.append(dynamic_path)

from api import app

client = TestClient(app)

def test_docs_redirect():
    client = TestClient(app)
    response = client.get("/")
    assert response.history[0].status_code == 307
    assert response.status_code == 200

def test_api():
    client = TestClient(app)

    # text = """But Google is starting from behind. The company made a late push 
    # into hardware, and Apple's Siri, available on iPhones, and Amazon's Alexa
    # software, which runs on its Echo and Dot devices, have clear leads in
    # consumer adoption."""

    text = """Google is starting from behind and Apple is far more productive. New-York is a great city that does not sleep"""

    request_data = {
        "values": [{"recordId": "a1", "data": {"text": text, "language": "en"}}]
    }
    


    # response = client.post("/entities", json=request_data)
    response = client.post("/entities_by_type", json=request_data)
    
    assert response.status_code == 200

    first_record = response.json()["values"][0]
    assert first_record["recordId"] == "a1"
    # assert first_record["errors"] == None
    # assert first_record["warnings"] == None

    # assert first_record["data"]["entities"] == [
    #     "Alexa",
    #     "Amazon",
    #     "Apple",
    #     "Echo and Dot",
    #     "Google",
    #     "iPhones",
    #     "Siri",
    # ]

    assert first_record["data"]["organizations"] == [
            "Google",
            "Apple",
            # "Amazon",
            # "Echo",
            # "Dot",
        ]

    assert first_record["data"]["gpes"] == [
            "New-York",
            ]


