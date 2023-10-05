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


python 003_ner_parsers_spacy_label_studio_generate.py

pip install -U spacy
pip install pandas


# to use displacy
pip install ipython


"""

import spacy
import pandas as pd
import json
from itertools import groupby

# Download spaCy models:
models = {
    'en_core_web_sm': spacy.load("en_core_web_sm"),
    'en_core_web_lg': spacy.load("en_core_web_lg")
}

# This function converts spaCy docs to the list of named entity spans in Label Studio compatible JSON format:
def doc_to_spans(doc):
    tokens = [(tok.text, tok.idx, tok.ent_type_) for tok in doc]
    results = []
    entities = set()
    for entity, group in groupby(tokens, key=lambda t: t[-1]):
        if not entity:
            continue
        group = list(group)
        _, start, _ = group[0]
        word, last, _ = group[-1]
        text = ' '.join(item[0] for item in group)
        end = last + len(word)
        results.append({
            'from_name': 'label',
            'to_name': 'text',
            'type': 'labels',
            'value': {
                'start': start,
                'end': end,
                'text': text,
                'labels': [entity]
            }
        })
        entities.add(entity)

    return results, entities


# Now load the dataset and include only lines containing "Easter ":
df = pd.read_csv('lines_clean_1.csv')
df = df[df['line_text'].str.contains("Easter ", na=False)]
print(df.head())
texts = df['line_text']

# Prepare Label Studio tasks in import JSON format with the model predictions:
entities = set()
tasks = []
for text in texts:
    predictions = []
    for model_name, nlp in models.items():
        doc = nlp(text)
        spans, ents = doc_to_spans(doc)
        entities |= ents
        predictions.append({'model_version': model_name, 'result': spans})
    tasks.append({
        'data': {'text': text},
        'predictions': predictions
    })

# Save Label Studio tasks.json
print(f'Save {len(tasks)} tasks to "tasks.json"')
with open('tasks.json', mode='w') as f:
    json.dump(tasks, f, indent=2)

# Save class labels as a txt file
print('Named entities are saved to "named_entities.txt"')
with open('named_entities.txt', mode='w') as f:
    f.write('\n'.join(sorted(entities)))
    
    


