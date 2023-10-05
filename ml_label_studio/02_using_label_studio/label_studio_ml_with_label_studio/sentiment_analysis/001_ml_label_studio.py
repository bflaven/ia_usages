#!/usr/bin/python
# -*- coding: utf-8 -*-
#

"""
[env]
# Conda Environment
conda create --name ml_with_label_studio python=3.9.13
conda info --envs
source activate ml_with_label_studio
conda deactivate


# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]

# update conda 
conda update -n base -c defaults conda


# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt


# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ml_label_studio/ml_with_label_studio/sentiment_analysis/


python 001_ml_label_studio.py

"""

from sentiment_cnn import SentimentCNN

model = SentimentCNN(state_dict='data/cnn.pt', vocab='data/vocab_obj.pt')
result = model.predict_sentiment("Label Studio is the best!")
# result = model.predict_sentiment("Bruno Flaven is an not a good ML engineer!")

print("\n --- result")
print(result)


