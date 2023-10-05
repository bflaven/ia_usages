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
cd /Users/brunoflaven/Documents/01_work/blog_articles/ml_label_studio/02_using_label_studio/

# [command]
python 03_convert_spacy_using_visualize_new_ner.py

# for chatgpt 
In python, write a script to read a local txt file named "sample.txt" to load it into a spacy like so "doc = nlp(document)" where document is the content of the txt file, be aware that file is encoded in utf-8.
"""

import spacy
from tqdm import tqdm
import urllib
import json
from spacy import displacy


# SET THE VALUES
INPUTFILE_DISPLACY_SOURCE = "label_studio_source_text_file/source_pt_johnidm_3.txt"
OUTPUTFILE_DISPLACY_HTML = 'PT_using_label_studio_data_custom_ner_01.html'



# Load the custom NER model
nlp = spacy.load("spacy_model_output/model-best")

# Read the content of the text file
with open(INPUTFILE_DISPLACY_SOURCE, "r", encoding="utf-8") as file:
    document = file.read()

doc = nlp(document)
colors = {"CRYPTO": "linear-gradient(315deg, #f5d020, #f53803)"}
options = {"ents": ["CRYPTO"], "colors": colors}

# colors = {"ORG": "linear-gradient(315deg, #f5d020, #f53803)"}
# options = {"ents": ["ORG"], "colors": colors}

# PER
# ORG


data = spacy.displacy.render(doc, style="ent", options=options, jupyter=False)
# ouput in an html file
with open(OUTPUTFILE_DISPLACY_HTML, "w") as file:
    file.write(data)

print(f'Output has been created with {OUTPUTFILE_DISPLACY_HTML} successfully.')
