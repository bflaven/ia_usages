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
python 008_ia_spacy_llm.py

# source
https://github.com/explosion/spacy-llm/pull/465




Available names: spacy.Ada.v1, spacy.Ada.v2, spacy.Azure.v1, spacy.Azure.v2, spacy.Babbage.v1, spacy.Babbage.v2, spacy.Claude-1-0.v1, spacy.Claude-1-0.v2, spacy.Claude-1-2.v1, spacy.Claude-1-2.v2, spacy.Claude-1-3.v1, spacy.Claude-1-3.v2, spacy.Claude-1.v1, spacy.Claude-1.v2, spacy.Claude-2.v1, spacy.Claude-2.v2, spacy.Claude-instant-1-1.v1, spacy.Claude-instant-1-1.v2, spacy.Claude-instant-1.v1, spacy.Claude-instant-1.v2, spacy.Code-Davinci.v1, spacy.Code-Davinci.v2, spacy.Command.v1, spacy.Command.v2, spacy.Curie.v1, spacy.Curie.v2, spacy.Davinci.v1, spacy.Davinci.v2, spacy.Dolly.v1, spacy.Falcon.v1, spacy.GPT-3-5.v1, spacy.GPT-3-5.v2, spacy.GPT-3-5.v3, spacy.GPT-4.v1, spacy.GPT-4.v2, spacy.GPT-4.v3, spacy.Llama2.v1, spacy.Mistral.v1, spacy.NoOp.v1, spacy.OpenLLaMA.v1, spacy.PaLM.v1, spacy.PaLM.v2, spacy.StableLM.v1, spacy.Text-Ada.v1, spacy.Text-Ada.v2, spacy.Text-Babbage.v1, spacy.Text-Babbage.v2, spacy.Text-Curie.v1, spacy.Text-Curie.v2, spacy.Text-Davinci.v1, spacy.Text-Davinci.v2, spacy.Text-Davinci.v3



"""
import spacy
from dotenv import load_dotenv
from spacy_llm.pipeline import LLMWrapper
from spacy_llm.registry import registry

# Load environment variables from .env file
load_dotenv()

# Load the English language model
nlp = spacy.load('en_core_web_sm')
print("\n --- result_1")
print("EN spacy loaded")

# Define and register custom task and model creation functions
@registry.llm_tasks("custom_ner_task")
def create_ner_task():
    return registry.llm_tasks.get("spacy.NER.v3")(labels=["PERSON", "ORGANISATION", "LOCATION"])

@registry.llm_models("custom_openai_model")
def create_openai_model():
    return registry.llm_models.get("spacy.GPT-3-5.v1")(name="gpt-3.5-turbo")

# Ensure 'llm_ner' is not already in the pipeline
if 'llm_ner' not in nlp.pipe_names:
    nlp.add_pipe(
        "llm_ner",
        config={
            "task": {"@llm_tasks": "custom_ner_task"},
            "model": {"@llm_models": "custom_openai_model"}
        },
        last=True
    )

# Example usage
doc = nlp("John Doe works at OpenAI in San Francisco.")
for ent in doc.ents:
    print(ent.text, ent.label_)



