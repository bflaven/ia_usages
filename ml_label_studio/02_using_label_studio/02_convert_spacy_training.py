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

python 02_convert_spacy_training.py



In python count the number of item in a json object

[
  [
    "text_data_1",
    {
      "entities":[
        [
          start,
          end,
          "labels"
        ]
      ]
    }
  ],
  [
    "text_data_2",
    {
      "entities":[
        [
          start,
          end,
          "labels"
        ]
      ]
    }
  ]
]

"""
 
# require for Spacy training
import spacy
from spacy.tokens import DocBin
from tqdm import tqdm

# JSON data
import json

# SET THE VALUES
INPUTFILE_SPACY_JSON = 'spacy_output_format_crypto.json'



with open(INPUTFILE_SPACY_JSON, 'r') as f:

    # Parse JSON data
    data = json.load(f)
    
    # debug    
    # print(data)
    
    count_items = len(data)
    print("Number of items in the JSON object:", count_items)


TRAIN_DATA = data[:4]
DEV_DATA = data[4:]

print('\n--- TRAIN_DATA')
print(TRAIN_DATA)

print('\n--- DEV_DATA')
print(DEV_DATA)

    
# train data
def convert(path, dataset):
    nlp = spacy.blank("pt")
    db = DocBin()
    for text, annot in tqdm(dataset):
        doc = nlp.make_doc(text)
        ents = []
        for start, end, label in annot["entities"]:
            span = doc.char_span(start, end, label=label, alignment_mode="contract")
            if span is None:
                print("Skipping entity")
            else:
                ents.append(span)
                doc.ents = ents
                db.add(doc)
                db.to_disk(path)

print(f'Output has been created with {INPUTFILE_SPACY_JSON} successfully.')

convert("spacy_split_output/train.spacy", TRAIN_DATA)
convert("spacy_split_output/dev.spacy", DEV_DATA)


