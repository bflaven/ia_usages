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
cd /Users/brunoflaven/Documents/03_git/BlogArticlesExamples/fastapi_nlp_model/017_chatGPT_fastapi_nlp_model/

# LAUNCH THE API
uvicorn nlp_api:app --reload

Check http://127.0.0.1:8000/docs


# lauch the test
python -m pytest --disable-warnings
pytest -q tests/test_nlp_api.py --disable-warnings


# install testing
pip install httpx
pip install starlette


"""
# import setuptools
# import pkg_resources

import json
import pytest
# from PIL import Image
# import pandas as pd
import sys
import os
import io

from fastapi.testclient import TestClient
# pytest app import fix
dynamic_path = os.path.abspath('.')
# print(dynamic_path)

sys.path.append(dynamic_path)

from nlp_api import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200

################################ Fixtures #####################################################
# in use
@pytest.fixture
def test_client():
    return TestClient(app)

# not in use
@pytest.fixture(scope="session")  
def input_json():  
    return json.dumps({"name": "Eric", "age": 32, "city": "London"})

# not in use
@pytest.fixture
def test_lang():
        test_lang == "fr"
        return test_lang

def test_healthcheck(test_client):
    """
    This test function is used to test the /healthcheck endpoint of the application.
    It uses the test client to send a GET request to the endpoint and then asserts that the response has a status code of 200 and a json payload of {"healthcheck": "Everything OK!"}
    This function is important to check if the application is running correctly and all the dependencies are working as expected.
    """
    # Send a GET request to the '/healthcheck' endpoint
    response = test_client.get("/healthcheck")
    # Assert that the response has a status code of 200
    assert response.status_code == 200
    # Assert that the response has a json payload of {"healthcheck": "Everything OK!"}
    assert response.json() == {"healthcheck": "Everything OK!"}

def test_redirect(test_client):
    # Send a GET request to the '/healthcheck' endpoint
    response = test_client.get("/docs")
    # Assert that the response has a status code of 200
    assert response.status_code == 200


