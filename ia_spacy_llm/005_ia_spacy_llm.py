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


# other libraries
python -m pip install spacy 
python -m pip install spacy-llm 
python -m pip install scikit-learn
python -m pip install python-dotenv
python -m pip install langchain-openai

# spacy
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_md
python -m spacy validate

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_spacy_llm/


# launch the file
python 005_ia_spacy_llm.py

# source
https://github.com/cbrew/spacy_llm_demos/blob/main/main.py


"""

from dotenv import load_dotenv
import spacy
def main():
    """
    :see https://spacy.io/api/large-language-models
    :return:
    """
    load_dotenv()
    nlp = spacy.blank("en")
    llm = nlp.add_pipe("llm_textcat")
    llm.add_label("INSULT")
    llm.add_label("COMPLIMENT")
    doc = nlp("You look gorgeous!")
    print(doc.cats)
    # {"COMPLIMENT": 1.0, "INSULT": 0.0}


if __name__ == '__main__':
    main()


