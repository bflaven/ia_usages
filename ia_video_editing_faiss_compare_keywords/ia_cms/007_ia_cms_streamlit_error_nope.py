#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
[env]
# Conda Environment
conda create --name ia_using_faiss python=3.9.13
conda info --envs
source activate ia_using_faiss
conda deactivate


# BURN AFTER READING
source activate ia_using_faiss

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n ia_using_faiss

# BURN AFTER READING
conda env remove -n ia_using_faiss


# install packages with conda
conda install -c conda-forge sentence-transformers
conda install -c pytorch faiss-cpu

# install packages with pip
python -m pip install sentence-transformers
python -m pip install pytorch faiss-cpu
python -m pip install numpy

python -m pip install huggingface_hub==0.25.2


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_video_editing_faiss_compare_keywords/ia_cms

# launch the file in streamlit
streamlit run 007_ia_cms_streamlit.py



"""

import streamlit as st
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Tuple

# Define the app title and set the layout to full screen
st.set_page_config(page_title="Semantic Keyword Search", layout="wide")

# Display package versions in an info box
st.info(f"""
    - faiss version: {faiss.__version__}
    - numpy version: {np.__version__}
    - SentenceTransformer version: {SentenceTransformer.__version__}
""")

# Main title of the app
st.title("Semantic Keyword Search")

# Define the tabs
tabs = st.tabs(["Search", "Archives"])

# Function to load keywords from a JSON file
def load_keywords_from_json(file_path: str) -> List[str]:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return [
        keyword['label'].strip('"')
        for keyword in data['keywords']
        if keyword['label'].strip('"')  # This condition excludes empty strings
    ]

# Function to get similar keywords
def get_similar_keywords(ia_generated_kw: List[str], cms_existing_kw: List[str]) -> List[Tuple[str, float, str]]:
    model = SentenceTransformer('all-MiniLM-L6-v2')
    ia_embeddings = model.encode(ia_generated_kw)
    cms_embeddings = model.encode(cms_existing_kw)
    faiss.normalize_L2(ia_embeddings)
    faiss.normalize_L2(cms_embeddings)
    dimension = ia_embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(cms_embeddings)
    k = len(cms_existing_kw)
    distances, indices = index.search(ia_embeddings, k)
    similar_keywords = []
    for i, (dist_row, idx_row) in enumerate(zip(distances, indices)):
        for j, (dist, idx) in enumerate(zip(dist_row, idx_row)):
            similar_keywords.append((cms_existing_kw[idx], float(dist), ia_generated_kw[i]))
    seen = {}
    unique_similar_keywords = []
    for kw, sim, orig in similar_keywords:
        if kw not in seen or sim > seen[kw][0]:
            seen[kw] = (sim, orig)
    for kw, (sim, orig) in seen.items():
        unique_similar_keywords.append((kw, sim, orig))
    unique_similar_keywords.sort(key=lambda x: x[1], reverse=True)
    return unique_similar_keywords

# Load keywords from JSON file
json_file_path = 'pt_tags_thema_list_4.json'
cms_existing_kw = load_keywords_from_json(json_file_path)

# IA CHOICE
ia_generated_kw = [
    "Hélio Almeida",
    "ministro das Finanças",
    "Presidente da República",
    "Carlos Vila Nova",
    "primeiro-ministro",
    "Patrice Trovoada",
    "ADI",
    "eleições 2022",
    "eleições antecipadas",
    "Tribunal Constitucional",
    "Hélio Vaz de Almeida",
    "economia",
    "Universidade Independente de Lisboa",
    "ministro do Plano e Finanças",
    "MLSTP",
    "Gabriel Costa",
    "Banco Central",
    "Jorge Bom Jesus",
    "Agência Fiduciária de Administração de Projetos",
    "AFAP"
]

# Tab 1: Search
with tabs[0]:
    st.header("Search")
    user_input = st.text_area("Enter keywords (one per line):", "\n".join(ia_generated_kw))
    st.write("Example keywords to copy and paste:")
    st.code("\n".join(ia_generated_kw))

    if st.button("Launch Semantic Similarity", type="primary", use_container_width=True, key="launch_button"):
        user_keywords = user_input.split("\n")
        similar_keywords = get_similar_keywords(user_keywords, cms_existing_kw)

        st.success("Semantic similarity operation completed!")

        st.write("Sorted list of keywords from cms_existing_kw with similarities:")
        for kw, sim, orig in similar_keywords:
            st.write(f"'{kw}' (Similarity: {sim:.4f}) - Original: '{orig}'")

        most_similar_keywords = [kw for kw, _, _ in similar_keywords]
        st.write("\nOrdered list of most similar keywords:")
        st.write(most_similar_keywords)

        reduced_most_similar_keywords = [kw for kw, sim, _ in similar_keywords if sim >= 0.8]
        st.write("\nReduced list of most similar keywords (Similarity >= 0.8):")
        st.write(reduced_most_similar_keywords)

        if st.button("Reset", use_container_width=True, key="reset_button"):
            st.experimental_rerun()

# Tab 2: Archives
with tabs[1]:
    st.header("Archives")
    st.write("This tab is reserved for future use.")







    
