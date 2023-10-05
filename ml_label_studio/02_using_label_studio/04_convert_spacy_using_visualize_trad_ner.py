#!/usr/bin/python
# -*- coding: utf-8 -*-
#

"""
[ENV_1]
# Conda Environment
conda create --name using_label_studio python=3.9.13
conda info --envs
source activate using_label_studio
conda deactivate

[ENV_2]
# Conda Environment
conda create --name tagging_entity_extraction python=3.9.13
conda info --envs
source activate tagging_entity_extraction
conda deactivate


# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]

# update conda
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements_using_label_studio.txt

# to install
pip install -r requirements_using_label_studio.txt

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ml_label_studio/BlogArticlesExamples/ml_label_studio/02_using_label_studio/



# [command]
python 04_convert_spacy_using_visualize_trad_ner.py

"""


import spacy
from tqdm import tqdm
import urllib
import json
from spacy import displacy


import spacy


# SET THE VALUES
INPUTFILE_DISPLACY_SOURCE = "label_studio_source_text_file/source_pt_johnidm_3.txt"



# INPUTFILE_DISPLACY_SOURCE = "label_studio_source_text_file/source_african_football_2.txt"

# INPUTFILE_DISPLACY_SOURCE = "label_studio_source_text_file/source_orange_confusion_fr_1.txt"

OUTPUTFILE_DISPLACY_HTML = 'PT_using_label_studio_data_trad_ner_01.html'


# nlp = spacy.load("en_core_web_sm")
nlp = spacy.load("pt_core_news_md")
# nlp = spacy.load("fr_core_news_md")


# Read the content of the text file
with open(INPUTFILE_DISPLACY_SOURCE, "r", encoding="utf-8") as file:
    document = file.read()

doc = nlp(document)

# colors = {"PERSON": "linear-gradient(90deg, #aa9cfc, #fc9ce7)"}
# options = {"ents": ["PERSON"], "colors": colors}

# data = spacy.displacy.render(doc, style="ent", options=options, jupyter=False)
data = spacy.displacy.render(doc, style="ent", jupyter=False)

with open(OUTPUTFILE_DISPLACY_HTML, "w") as file:
    file.write(data)

print(f'Output has been created with {OUTPUTFILE_DISPLACY_HTML} successfully.')

