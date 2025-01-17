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
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_video_editing_faiss_compare_keywords/ia_cms


# launch the file
python 002_ia_cms.py




"""

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Initialize the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Define the input lists
ia_generated_kw = ['Milagre económico', 'Ásia-Pacífico', 'Ásia-Pacífico', 'persona non grata".', 'Ébola', 'Áudio', 'óleo de palma', 'Áustria']
cms_existing_kw = ['Milagre económico', 'agentes do estrangeiro', '1° de Maio', 'persona non grata".', 'phygital', '#Metoopolitico', 'óleo de palma', 'ABBA']

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
k = 1  # Number of nearest neighbors to retrieve
distances, indices = index.search(ia_embeddings, k)

# Create a list to store the most similar keywords
most_similar_keywords = []

# Threshold for similarity (adjust as needed)
similarity_threshold = 0.7

for i, idx in enumerate(indices):
    if distances[i][0] > similarity_threshold:
        most_similar_keywords.append(cms_existing_kw[idx[0]])

# Remove duplicates while preserving order
most_similar_keywords = list(dict.fromkeys(most_similar_keywords))

print("Most similar keywords from cms_existing_kw:")
print(most_similar_keywords)











    
