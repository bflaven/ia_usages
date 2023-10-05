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

# installe flair
pip install flair

# check the install for Spacy
python -m spacy validate

# LAUNCH THE API
python flair_sentiment_sample.py


"""
from flair.models import TextClassifier
from flair.data import Sentence

# For Flair, you load models in advance.
# Note that this is memory intensive and can take some time
sentiment_model = TextClassifier.load("en-sentiment")

# We're going to analyse these two texts for sentiment
sample_text = [
    "I love using Python to make really fast APIs.",
    "I hate silly bugs that happen and annoy me."
]

# Simply iterate through the samples, and run the prediction
for text in sample_text:
    # For Flair, you convert your raw data into "sentences" prior to analysis
    sentence = Sentence(text)
    # This is the analysis step, note that it edits the sentence to include the
    # prediction
    sentiment_model.predict(sentence)
    print(f"The sentence '{text}' is detected as {sentence.labels[0]}.")
