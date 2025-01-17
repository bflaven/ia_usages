#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
[env]
# Conda Environment
conda create --name ia_using_faiss python=3.9.13
conda info --envs
source activate ia_using_faiss
source activate clip_env
conda deactivate


# BURN AFTER READING
source activate ia_using_faiss

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n ia_using_faiss
conda env remove -n ia_using_clip
conda env remove -n clip_env


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
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_video_editing_faiss_compare_keywords/ia_faiss/


# launch the file
python 004_ia_faiss.py

https://github.com/bflaven/ia_usages/tree/921276b19f5098e990588a7061511ae80af7eb7a/ia_spacy_llm



"""

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Sample text documents
documents = [
    "The quick brown fox jumps over the lazy dog",
    "A journey of a thousand miles begins with a single step",
    "To be or not to be, that is the question",
    "All that glitters is not gold",
    "Where there's a will, there's a way"
]

# Initialize the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings for the documents
document_embeddings = model.encode(documents)

# Create a Faiss index
dimension = document_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)

# Add document embeddings to the index
index.add(document_embeddings.astype('float32'))

# Function to perform similarity search
def semantic_search(query, top_k=2):
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding.astype('float32'), top_k)
    return [(documents[i], distances[0][j]) for j, i in enumerate(indices[0])]

# Example usage
query = "What is the meaning of life?"
results = semantic_search(query)

print(f"Query: {query}")
print("Top 2 similar documents:")
for doc, distance in results:
    print(f"- {doc} (Distance: {distance:.4f})")










    
