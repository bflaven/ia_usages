#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
conda create --name llm_integration_api_costs python=3.9.13
conda info --envs
source activate fmm_fastapi_poc
conda deactivate


# BURN AFTER READING
source activate fmm_fastapi_poc



# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n llm_integration_api_costs

# BURN AFTER READING
conda env remove -n mistral_integration


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# manual install
pip install openai
pip install mistralai
pip install langchain-mistralai
pip install beautifulsoup4

python -m pip install beautifulsoup4
python -m pip install openai

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_build_vue_js_on_fastapi/streamlit_module_annotated_text/


# launch the file
streamlit run example_2.py


https://github.com/tvst/st-annotated-text


"""

import streamlit as st
from annotated_text import annotated_text
import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def process_text(text):
    """Process the text and return annotated elements and detected entities."""
    doc = nlp(text)
    
    annotated_elements = []
    detected_entities = []

    # Iterate over the tokens in the doc and annotate entities
    for token in doc:
        if token.ent_type_:
            annotated_elements.append((token.text, token.ent_type_))
        else:
            annotated_elements.append(token.text)
        annotated_elements.append(" ")  # Add a space after each token
    
    # Remove the trailing space for the last element
    if annotated_elements[-1] == " ":
        annotated_elements = annotated_elements[:-1]

    # Collect detected entities
    for entity in doc.ents:
        detected_entities.append((entity.text, entity.label_))
    
    return annotated_elements, detected_entities

# Sample text for analysis
# Here is a sample sentence with some entities:
# sample_text = "I was walking down 5th Avenue yesterday in New York City and I saw Bill Gates!"
sample_text = "Apple is looking at buying U.K. startup for $1 billion"
# sample_text = "Alphabet sets profit record, plans $50 billion buyback"
# sample_text = "In the USA, TikTok Rankles Employees With Return-to-Office Tracking Tools. The company is requiring many employees to use an app that tracks their in-person attendance."


# Process the text
annotated_elements, detected_entities = process_text(sample_text)

# Display the annotated text using Streamlit
st.write("## Annotated Text:")
with st.echo():
    annotated_text(*annotated_elements)

# Display detected entities separately
st.write("## Detected Entities:")
for text, label in detected_entities:
    st.write(f"Entity Detected: {text}, Type: {label}")

