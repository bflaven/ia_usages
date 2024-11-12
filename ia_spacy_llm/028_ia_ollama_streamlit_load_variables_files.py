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
streamlit run 028_ia_ollama_streamlit_load_variables_files.py

# source
https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
https://medium.com/@rahultiwari065/unlocking-the-power-of-sentence-embeddings-with-all-minilm-l6-v2-7d6589a5f0aa
https://docs.streamlit.io/develop/api-reference



# EXAMPLES

# EXAMPLE_1
title: 
Kylian Mbappé left out of France squad for Israel and Italy games
keywords: 
France, Kylian Mbappé, football, Real Madrid, UEFA Nations League
content: 
Struggling to make an impact at Real Madrid, star striker Kylian Mbappé has been left out of the France squad for their upcoming matches against Israel and Italy for the UEFA Nations League.


# EXAMPLE_2
title: Ukrainian defences in Donbas risk getting steamrolled by Russian advance
keywords: Ukraine war analysis, Ukraine, Russia, Donbas, Donetsk
content: As Russian troops chart a steady advance in east Ukraine, worn-down Ukrainian forces are struggling to plug holes in their front-line defences. At stake is the "fortress" town of Pokrovsk, a transport and logistics hub that could give Russia a clear pathway to advance in the Donetsk region and beyond.



# EXAMPLE_3
title: Iran arrests female student who stripped to protest dress code
keywords: Iran, women, women's rights, Mahsa Amini, Afghanistan, Middle East, protest
content: Iranian authorities on Saturday arrested a female student who staged a solo protest by stripping to her underwear in public. Reports indicate the action aimed to highlight the oppressive enforcement of Iran's dress code, which mandates women wear a headscarf and loose-fitting clothing in public.


# EXAMPLE_4 (french for sanitize)
title: 
"Les garde-fous ont disparu" : l'UE se prépare face à l'hypothèse d'une victoire de Trump

keywords: 
Union européenne, Pour aller plus loin, États-Unis, Présidentielle américaine, USA 2024, Donald Trump, Décryptage, l'été dernier

content:
Lors de son mandat à la Maison Blanche, Donald Trump avait retiré les États-Unis de plusieurs accords internationaux et agences de l'ONU, menaçant même de quitter l'Otan. À l'époque, des hauts fonctionnaires de son équipe agissaient comme "garde-fous" et l'Europe n'était pas en proie à un conflit sur son territoire. Aujourd'hui, face à la possibilité d'un retour au pouvoir du milliardaire, l'Europe se prépare activement à se protéger d'une nouvelle présidence du républicain.





"""

import os
import ast
import streamlit as st

# Define the directory path
directory = "ollama_output"

# Get a list of Python files in the directory
python_files = [f for f in os.listdir(directory) if f.endswith(".py")]

# Create a selectbox for the user to choose a file
selected_file = st.selectbox("Select a file", python_files)

# If a file is selected, load the variables from the file
if selected_file:
    with open(os.path.join(directory, selected_file), "r") as f:
        content = f.read()

    # Parse the variables from the file content
    variables = {}
    tree = ast.parse(content)
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    variables[target.id] = ast.literal_eval(node.value)

    # Print out the values for each variable
    st.write("Title Proposals:")
    st.write(variables["title_proposals"])

    st.write("Keywords Combinations:")
    st.write(variables["keywords_combinations"])

    st.write("Best Content:")
    st.code(variables["best_content"])

    st.write("Best Title:")
    st.code(variables["best_title"])

    st.write("Best Keywords:")
    st.write(variables["best_keywords"])




