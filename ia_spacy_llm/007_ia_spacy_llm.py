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
python 007_ia_spacy_llm.py

# source
https://github.com/explosion/spacy-llm/pull/465

ollama list
ollama serve
ollama pull notus


Available names: spacy.Ada.v1, spacy.Ada.v2, spacy.Azure.v1, spacy.Azure.v2, spacy.Babbage.v1, spacy.Babbage.v2, spacy.Claude-1-0.v1, spacy.Claude-1-0.v2, spacy.Claude-1-2.v1, spacy.Claude-1-2.v2, spacy.Claude-1-3.v1, spacy.Claude-1-3.v2, spacy.Claude-1.v1, spacy.Claude-1.v2, spacy.Claude-2.v1, spacy.Claude-2.v2, spacy.Claude-instant-1-1.v1, spacy.Claude-instant-1-1.v2, spacy.Claude-instant-1.v1, spacy.Claude-instant-1.v2, spacy.Code-Davinci.v1, spacy.Code-Davinci.v2, spacy.Command.v1, spacy.Command.v2, spacy.Curie.v1, spacy.Curie.v2, spacy.Davinci.v1, spacy.Davinci.v2, spacy.Dolly.v1, spacy.Falcon.v1, spacy.GPT-3-5.v1, spacy.GPT-3-5.v2, spacy.GPT-3-5.v3, spacy.GPT-4.v1, spacy.GPT-4.v2, spacy.GPT-4.v3, spacy.Llama2.v1, spacy.Mistral.v1, spacy.NoOp.v1, spacy.OpenLLaMA.v1, spacy.PaLM.v1, spacy.PaLM.v2, spacy.StableLM.v1, spacy.Text-Ada.v1, spacy.Text-Ada.v2, spacy.Text-Babbage.v1, spacy.Text-Babbage.v2, spacy.Text-Curie.v1, spacy.Text-Curie.v2, spacy.Text-Davinci.v1, spacy.Text-Davinci.v2, spacy.Text-Davinci.v3



"""

from spacy_llm.util import assemble

nlp = assemble("config_2.cfg")

doc = nlp("In early April, Amazon announced plans to expand its operations into Delft, Netherlands, aiming to strengthen its technology hub in Europe. The CEO, Andy Jassy, mentioned during a press conference at The Hague that this move would create over 500 new jobs in the region by the end of 2024. Meanwhile, in a related development, Microsoft, under the leadership of Satya Nadella, has launched a new cloud computing service in partnership with the University of Cambridge. This collaboration aims to facilitate advanced research in artificial intelligence and machine learning applications.")

print([(ent.text, ent.label_) for ent in doc.ents])



