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
python get_entities_and_sentment.py


"""
from typing import Tuple, List

from typing import Tuple, List
from flair.models import TextClassifier
from flair.data import Sentence
import spacy

nlp = spacy.load("en_core_web_sm")
sentiment_model = TextClassifier.load('en-sentiment')


def get_entities_and_sentiment(text: str) -> Tuple[dict, List[dict]]:
    """Parse a string, and determine sentiment polarity and entities contained within"""
    doc = nlp(text)
    entity_list = [
        {"name": x.text, "type": x.label_} for x in doc.ents
    ]
    sentence = Sentence(text)
    sentiment_model.predict(sentence)
    label = sentence.labels[0]
    sentiment = {'sentiment': label.value, 'polarity': label.score}
    return sentiment, entity_list


# Run a small test
if __name__ == '__main__':
    # We're testing if our sentiment and entity function is working correctly:
    result = get_entities_and_sentiment("I travelled to New York and I hated it.")
    print(result)
