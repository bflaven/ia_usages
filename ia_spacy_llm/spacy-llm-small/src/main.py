#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
[env]
# Conda Environment
conda create --name ia_spacy_llm python=3.9.13
conda info --envs
source activate ia_spacy_llm
conda deactivate


# BURN AFTER READING
source activate ia_spacy_llm

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n ia_spacy_llm

# BURN AFTER READING
conda env remove -n ia_spacy_llm


python -m pip install spacy 
python -m pip install spacy-llm 
python -m pip install scikit-learn
python -m spacy download en_core_web_sm
python -m pip install python-dotenv
python -m pip install langchain-openai
python -m pip install pytextrank
pip install pytextrank


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_spacy_llm/spacy-llm-small


# launch the file
python 001_ia_spacy_llm.py

# source
https://github.com/patmejia/spacy-llm/tree/main

pytest src/test.py
python src/main.py
python src/get_top_ranked_phrases.py


"""

import spacy
import pytextrank
from pprint import pprint


def load_model():
    return spacy.load("en_core_web_sm")


def process_text(nlp, text):
    return nlp(text)


def process_text_returns_expected_tuples(nlp, text):
    doc = process_text(nlp, text)
    return [(token.text, token.pos_, token.dep_) for token in doc]


def extract_entities_returns_expected_entity_tuples(nlp, text):
    doc = process_text(nlp, text)
    return [(ent.text, ent.label_) for ent in doc.ents]


def summarize_text_returns_expected_summary(nlp, text):
    doc = process_text(nlp, text)
    if 'textrank' not in nlp.pipe_names:
        nlp.add_pipe("textrank")
    doc = nlp(text)
    return [str(sent) for sent in doc._.textrank.summary(limit_phrases=15, limit_sentences=5)]

        
def print_results(text, result, result_type, result_description):
    print("Text:\n")
    print(text)
    print("\nResult:\n")
    pprint(result[:5])
    print(f"\nEach element in the result is a {result_description}.")
    print(f'The text was processed into {len(result)} such {result_type}.\n\n')


def display_results(text):
    nlp = load_model()
    operations = {
        'tuples': {
            'function': process_text_returns_expected_tuples,
            'description': '3-tuple (token, part-of-speech tag, dependency tag)'
        },
        'entity tuples': {
            'function': extract_entities_returns_expected_entity_tuples,
            'description': '2-tuple (entity, entity type)'
        },
        'sentences': {
            'function': summarize_text_returns_expected_summary,
            'description': 'list of sentences that summarize the text'
        }
    }

    for result_type, operation in operations.items():
        result = operation['function'](nlp, text)
        print_results(text, result, result_type, operation['description'])


if __name__ == "__main__":
    

    # butyrate_text = """
    # Trivia: The bacterium Faecalibacterium prausnitzii in the human gut microbiome is responsible for producing butyrate, a short-chain fatty acid.
    # Explanation: Faecalibacterium prausnitzii utilizes complex carbohydrates, such as dietary fiber, as its primary energy source. Through a fermentation process, it breaks down these carbohydrates into smaller molecules, including butyrate. Butyrate has beneficial effects on gut health, serving as an energy source for colon cells, promoting their growth, maintaining the gut barrier integrity, and reducing inflammation. Faecalibacterium prausnitzii's ability to produce butyrate highlights its importance in maintaining a healthy gut microbiome.
    # """

    butyrate_text = """
    The share price of a small Chinese company in financial difficulties has skyrocketed in recent days. The company's only real asset is its name: Wisesoft, which in Chinese sounds like the phrase 'Trump wins big'. Chinese investors are prone to buying shares solely on the basis of a company name.

    Former US president Donald Trump’s influence looms large, and not just in the United States. In China, his name has prompted some people to make a quirky bet on the stock market.

    The share price of a small company that makes air traffic control software, Wisesoft, doubled over the past month on the Shenzhen Stock Exchange, a gain at odds with the company’s lacklustre financial results. It recorded a loss of Є3.5 million, (27.04 million yuan), for the first nine months of 2024.

    Wisesoft's attraction for local investors is in its name, phonetically close to the expression “Trump wins big”, notes Bloomberg News.
    """

    display_results(butyrate_text)
