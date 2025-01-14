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



# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_video_editing_faiss_compare_keywords/ia_cms/


# launch the file
python 004_ia_cms.py




"""

import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Tuple

def load_keywords_from_json(file_path: str) -> List[str]:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    return [
        keyword['label'].strip('"')
        for keyword in data['keywords']
        if keyword['label'].strip('"')  # This condition excludes empty strings
    ]

def get_similar_keywords(ia_generated_kw: List[str], cms_existing_kw: List[str]) -> List[Tuple[str, float, str]]:
    # Initialize the SentenceTransformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Encode the keywords
    ia_embeddings = model.encode(ia_generated_kw)
    cms_embeddings = model.encode(cms_existing_kw)

    # Normalize the vectors
    faiss.normalize_L2(ia_embeddings)
    faiss.normalize_L2(cms_embeddings)

    # Create a FAISS index
    dimension = ia_embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(cms_embeddings)

    # Perform the search
    k = len(cms_existing_kw)  # Search for all possible matches
    distances, indices = index.search(ia_embeddings, k)

    # Create a list to store the keywords with their similarities
    similar_keywords = []

    for i, (dist_row, idx_row) in enumerate(zip(distances, indices)):
        for j, (dist, idx) in enumerate(zip(dist_row, idx_row)):
            similar_keywords.append((cms_existing_kw[idx], float(dist), ia_generated_kw[i]))

    # Remove duplicates while preserving the highest similarity
    seen = {}
    unique_similar_keywords = []
    for kw, sim, orig in similar_keywords:
        if kw not in seen or sim > seen[kw][0]:
            seen[kw] = (sim, orig)
    
    for kw, (sim, orig) in seen.items():
        unique_similar_keywords.append((kw, sim, orig))

    # Sort by similarity (highest to lowest)
    unique_similar_keywords.sort(key=lambda x: x[1], reverse=True)

    return unique_similar_keywords

# Load keywords from JSON file
json_file_path = 'pt_tags_thema_list_3.json'
cms_existing_kw = load_keywords_from_json(json_file_path)

# Define the IA generated keywords
ia_generated_kw = ['Milagre económico', 'Ásia-Pacífico', 'persona non grata', 'Ébola', 'Áudio', 'óleo de palma', 'Áustria']

# Get the sorted list of similar keywords with similarities
similar_keywords = get_similar_keywords(ia_generated_kw, cms_existing_kw)

# Print the results
print("Sorted list of keywords from cms_existing_kw with similarities:")
for kw, sim, orig in similar_keywords:
    print(f"'{kw}' (Similarity: {sim:.4f}) - Original: '{orig}'")

# If you need just the keywords in a list, you can do:
most_similar_keywords = [kw for kw, _, _ in similar_keywords]
print("\nOrdered list of most similar keywords:")
print(most_similar_keywords)














    
