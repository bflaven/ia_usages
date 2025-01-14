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
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_video_editing_faiss_compare_keywords/ia_faiss/


# launch the file
python 007_ia_faiss.py

# source
https://github.com/bflaven/ia_usages/tree/921276b19f5098e990588a7061511ae80af7eb7a/ia_spacy_llm



"""


from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load the pre-trained model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Define the best title and the title proposals
best_title = "German opposition demands confidence vote next week as Scholz's coalition crumbles"

title_proposals = [
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

# Generate embeddings for the best title and title proposals
best_title_embedding = model.encode([best_title])[0]
proposal_embeddings = model.encode(title_proposals)

# Create a Faiss index
d = best_title_embedding.shape[0]  # Dimensionality of the embeddings
index = faiss.IndexFlatL2(d)

# Add the proposal embeddings to the index
index.add(proposal_embeddings)

# Perform the search
k = 3  # Number of nearest neighbors to retrieve
D, I = index.search(best_title_embedding.reshape(1, -1), k)

# Calculate cosine similarity for the top 3 titles
similarities = cosine_similarity(best_title_embedding.reshape(1, -1), proposal_embeddings[I[0]])

# Get the top 3 most similar titles with their similarity scores
top_3_titles = [(title_proposals[i], similarities[0][j]) for j, i in enumerate(I[0])]

print("Top 3 most similar titles with similarity scores:")
for i, (title, score) in enumerate(top_3_titles, 1):
    print(f"{i}. {title}")
    print(f"   Similarity score: {score:.4f}")
    print()








    
