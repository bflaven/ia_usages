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
pip freeze > requirements_tagging_entity_extraction.txt

# to install
pip install -r requirements_tagging_entity_extraction.txt

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/using_label_studio_spacy/


# V1
python 04_convert_format_for_label_studio.py



# extra stuff
pip install jupyter 

"""


import json 
import pandas as pd
import sys


# V0
# df = pd.read_json(sys.argv[1], lines=True)
# DEBUG
# print(df)
# docs = [{ 'data': {'text': text } } for text in df['text']]

# SET THE VALUES
INPUTFILE_LABEL_STUDIO_SOURCE = "reddit_r_cooking_sample.jsonl"
OUTPUTFILE_LABEL_STUDIO = '002_label_studio_samples.json'

# V1

# Read the JSON file into a DataFrame
df = pd.read_json(INPUTFILE_LABEL_STUDIO_SOURCE, lines=True)

new_df = [{'data': {'text': text}} for text in df['text']]

# Output the result
# print(new_df)

# Output the list of JSON objects to a file
with open(OUTPUTFILE_LABEL_STUDIO, 'w') as f:
    json.dump(new_df, f)

print(f'Output has been created with {OUTPUTFILE_LABEL_STUDIO} successfully.')
