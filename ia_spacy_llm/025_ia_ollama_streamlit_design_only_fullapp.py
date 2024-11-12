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

# other
python -m pip install -U sentence-transformers

# ollama
https://pypi.org/project/ollama/
python -m pip install ollama

# streamlit
python -m pip install streamlit


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_spacy_llm/


# launch the file
streamlit run 025_ia_ollama_streamlit_design_only_fullapp.py

# source
https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
https://medium.com/@rahultiwari065/unlocking-the-power-of-sentence-embeddings-with-all-minilm-l6-v2-7d6589a5f0aa


https://docs.streamlit.io/develop/api-reference



# EXAMPLES

# EXAMPLE_1
title: Kylian Mbappé left out of France squad for Israel and Italy games
keywords: France, Kylian Mbappé, football, Real Madrid, UEFA Nations League
content: Struggling to make an impact at Real Madrid, star striker Kylian Mbappé has been left out of the France squad for their upcoming matches against Israel and Italy for the UEFA Nations League.


# EXAMPLE_2
title: Ukrainian defences in Donbas risk getting steamrolled by Russian advance
keywords: Ukraine war analysis, Ukraine, Russia, Donbas, Donetsk
content: As Russian troops chart a steady advance in east Ukraine, worn-down Ukrainian forces are struggling to plug holes in their front-line defences. At stake is the "fortress" town of Pokrovsk, a transport and logistics hub that could give Russia a clear pathway to advance in the Donetsk region and beyond.



# EXAMPLE_3
title: Iran arrests female student who stripped to protest dress code
keywords: Iran, women, women's rights, Mahsa Amini, Afghanistan, Middle East, protest
content: Iranian authorities on Saturday arrested a female student who staged a solo protest by stripping to her underwear in public. Reports indicate the action aimed to highlight the oppressive enforcement of Iran's dress code, which mandates women wear a headscarf and loose-fitting clothing in public.

"""

import streamlit as st

# Define a title with an icon
st.set_page_config(page_title="My App", page_icon=":guardsman:", layout="wide")

# Create three tabs
tab1, tab2, tab3 = st.tabs(["Send to LLM", "Similarity score", "Explanations"])

# Tab 1: Send to LLM
with tab1:
    user_input1 = st.text_input("Enter your text:", key="tab1_input")
    if st.button("Send to LLM", type="primary"):
        st.write("You entered: ", user_input1)
    if st.button("Reset", type="secondary"):
        user_input1 = ""

# Tab 2: Similarity score
with tab2:
    user_input2 = st.text_input("Enter your text:", key="tab2_input")
    if st.button("Refresh2", type="secondary"):
        user_input2 = ""
    if st.button("Submit2", type="primary"):
        st.write("You entered: ", user_input2)

# Tab 3: Explanations
with tab3:
    if st.button("Refresh3", type="secondary"):
        user_input3 = ""

    user_input3 = st.text_input("Enter your text:", key="tab3_input")
    if st.button("Submit3", type="primary"):
        st.write("You entered: ", user_input3)



