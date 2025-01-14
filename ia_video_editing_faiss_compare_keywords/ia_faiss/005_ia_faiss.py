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
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_video_editing_faiss_compare_keywords/ia_faiss/


# launch the file
python 005_ia_faiss.py

https://github.com/bflaven/ia_usages/tree/921276b19f5098e990588a7061511ae80af7eb7a/ia_spacy_llm



"""

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Sample text documents
documents = [
"CDU Calls for Confidence Vote in Germany Amid Coalition Crisis Following Finance Minister's Dismissal",
"Olaf Scholz Faces Confidence Vote as German Coalition Collapses After Finance Minister's Exit",
"German Government Crisis: CDU Demands Confidence Vote after Finance Minister Dismissal",
"Coalition Crumbles: Scholz Faces Confidence Vote as Germany's CDU Opposition Calls for Action",
"Scholz's Coalition on Brink of Collapse: Germany's CDU Opposition Seeks Confidence Vote",
"Germany's Political Crisis: Scholz Faces Confidence Vote after Finance Minister Dismissal",
"CDU Opposition Demands Confidence Vote in Germany as Coalition Crumbles Following Finance Minister's Departure",
"Scholz's Government on the Brink: CDU Seeks Confidence Vote Amid German Coalition Crisis",
"German Political Crisis: Scholz to Face Confidence Vote after Coalition Partner's Dismissal",
"Coalition Collapse: Germany's Scholz Faces Confidence Vote as CDU Calls for Action Following Finance Minister's Departure"
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
query = "What is the best title compared to this title \"German opposition demands confidence vote next week as Scholz's coalition crumbles\"? "
results = semantic_search(query)

print(f"Query: {query}")
print("Top 2 similar documents:")
for doc, distance in results:
    print(f"- {doc} (Distance: {distance:.4f})")










    
