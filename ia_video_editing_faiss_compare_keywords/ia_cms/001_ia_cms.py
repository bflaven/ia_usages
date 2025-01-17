#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
[env]
# Conda Environment
conda create --name ia_using_faiss python=3.9.13
conda info --envs
source activate ia_using_faiss
conda deactivate


# BURN AFTER READING
source activate ia_using_faiss

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n ia_using_faiss

# BURN AFTER READING
conda env remove -n ia_using_faiss


# install packages with conda
conda install -c conda-forge sentence-transformers
conda install -c pytorch faiss-cpu

# install packages with pip
python -m pip install sentence-transformers
python -m pip install pytorch faiss-cpu
python -m pip install numpy



# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_video_editing_faiss_compare_keywords/ia_cms


# launch the file
python 001_ia_cms.py




"""

import json

# Load the JSON file
with open('pt_tags_thema_list_3.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Extract non-empty keywords
cms_existing_kw = [
    keyword['label'].strip('"')
    for keyword in data['keywords']
    if keyword['label'].strip('"')  # This condition excludes empty strings
]

# Print the result
print("cms_existing_kw =", cms_existing_kw)








    
