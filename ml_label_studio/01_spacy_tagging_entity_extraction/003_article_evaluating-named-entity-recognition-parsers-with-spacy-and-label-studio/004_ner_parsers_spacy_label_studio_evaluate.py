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


[path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ml_label_studio/01_spacy_tagging_entity_extraction/003_annotate_tool_demo_label_studio_doccano/001_article_evaluating-named-entity-recognition-parsers-with-spacy-and-label-studio/


python 004_ner_parsers_spacy_label_studio_evaluate.py



pip install -U spacy
pip install pandas


# to use displacy
pip install ipython


"""

import json
from collections import defaultdict


tasks = json.load(open('annotations_1.json'))
model_hits = defaultdict(int)

for task in tasks:
    annotation_result = task['annotations'][0]['result']
    for r in annotation_result:
        r.pop('id')
    for prediction in task['predictions']:
        
        print(int(prediction))
        # MODEL
        # model_hits[prediction['model_version']] += int(prediction['result'] == annotation_result)
        
        

num_task = len(tasks)
for model_name, num_hits in model_hits.items():
    acc = num_hits / num_task
    print(f'Accuracy for {model_name}: {acc:.2f}%')
