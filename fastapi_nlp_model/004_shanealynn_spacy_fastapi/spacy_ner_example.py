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
conda env remove -n fastapi_datacamp

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements_ner_service.txt

# to install
pip install -r requirements_ner_service.txt

# [path]
cd /Users/brunoflaven/Documents/03_git/BlogArticlesExamples/fastapi_nlp_model/004_shanealynn_spacy_fastapi/

# install spacy
python -m spacy download en_core_web_sm


# check the install for Spacy
python -m spacy validate

# LAUNCH THE API
python spacy_ner_example.py


"""

import spacy
nlp = spacy.load("en_core_web_sm")

# Here is a sample sentence with some entities:
sample_text = "I was walking down 5th Avenue yesterday in New York City and I saw Bill Gates!"
# sample_text = "Apple is looking at buying U.K. startup for $1 billion"
# sample_text = "Alphabet sets profit record, plans $50 billion buyback"
# sample_text = "In the USA, TikTok Rankles Employees With Return-to-Office Tracking Tools. The company is requiring many employees to use an app that tracks their in-person attendance."

# sentences examples





# For Spacy, first turn your raw text data into a "document":
doc = nlp(sample_text)
# The document then "magically" has everything calculated:
for entity in doc.ents:
    print(f"Entity Detected: {entity.text}, of type: {entity.label_}")
