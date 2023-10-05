#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
conda create --name tagging_entity_extraction python=3.9.13
conda info --envs
source activate tagging_entity_extraction

conda deactivate
# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n chainlit_python
conda env remove -n ai_chatgpt_prompts

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > tagging_entity_extraction.txt



# to install
pip install -r tagging_entity_extraction.txt


cd /Users/brunoflaven/Documents/01_work/blog_articles/ml_label_studio/files_for_github_ml_label_studio/01_spacy_tagging_entity_extraction/


python 04_medium_demo_johnidouglasmarangon.py


# to use displacy
pip install ipython

# check the file
https://gist.github.com/johnidm/27e3b2ff50e592bc37183907ba97d31d


"""


import urllib
import json
import spacy 
import urllib 

nlp = spacy.load("pt_core_news_md")


url = "https://gist.githubusercontent.com/johnidm/0971d537443515fce71ab28907ecaef5/raw/f1cc41b94345516720bcc98c1984581f028b9486/dataset.json"

data = json.loads(urllib.request.urlopen(url).read().decode("utf-8"))

# 41 items in the dataset
dataset = data["annotations"]
TRAIN_DATA = dataset[:30]
DEV_DATA = dataset[30:]

# print('\n--- TRAIN_DATA')
# print(TRAIN_DATA)

# print('\n--- DEV_DATA')
# print(DEV_DATA)
