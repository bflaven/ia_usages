#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
# NO CONDA ENV

conda create --name tagging_entity_extraction python=3.9.13
conda info --envs
source activate tagging_entity_extraction

conda deactivate
# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]




# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > tagging_entity_extraction.txt



# to install
pip install -r tagging_entity_extraction.txt

[path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ai_chatgpt_prompts/project_6_spacy_experiences/

[file]
python 001_project_6_spacy_experiences.py



"""

# dependency.py
# python dependency.py
import spacy
nlp = spacy.load("en_core_web_sm")


doc = nlp(u'I have flown to LA. Now I am flying to Frisco.')
for token in doc:
  print("Text :: " + token.text, "\npos_ :: " +
        token.pos_, "\ndep_ :: " + token.dep_ + "\n\n")








