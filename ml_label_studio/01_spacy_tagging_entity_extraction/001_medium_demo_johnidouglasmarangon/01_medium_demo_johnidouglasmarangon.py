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



python 01_medium_demo_johnidouglasmarangon.py


# to use displacy
pip install ipython

"""

import spacy
from spacy import displacy

nlp = spacy.load("pt_core_news_md")

# print(nlp.pipe_names)

# text = """ O Bitcoin (BTC) recuperou parte das perdas registradas em meio à batalha regulatória. """

""" EXAMPLE_1
doc = nlp(text) 
print(doc.ents)
"""


doc = nlp(""" Meu nome é Johnny B. Goode e hoje estou tocando em Hollywood no Teatro Álvaro de Carvalho """) 
# for ent in doc.ents: 
#     print(f"{ent.label_} : {ent.text}")
    
    

colors = {"PER": "linear-gradient(90deg, #aa9cfc, #fc9ce7)"}
options = {"colors": colors} 
data = displacy.render(doc, style="ent", jupyter=False, options=options)

with open("data_01.html", "w") as file:
    file.write(data)
    
    
    
# nlp = spacy.load("en_core_web_sm")
# doc = nlp(u'This is a sentence.')

# doc = nlp(u'Rats are various medium-sized, long-tailed rodents.')
# displacy.render(doc, style='dep',jupyter=True)