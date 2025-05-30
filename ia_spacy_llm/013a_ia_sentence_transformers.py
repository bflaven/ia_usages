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



# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_spacy_llm/


# launch the file
python 013a_ia_sentence_transformers.py

# source
https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
https://medium.com/@rahultiwari065/unlocking-the-power-of-sentence-embeddings-with-all-minilm-l6-v2-7d6589a5f0aa


"""
from sentence_transformers import SentenceTransformer, util

# Load the model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

best_title = "Harris falls short as US election exposes cracks in anti-Trump coalition"
title_proposals = [
    "Trump's Resurgence: US Election Reveals Cracks in Anti-Trump Coalition",
    "The Fragmented Democratic Coalition: Kamala Harris Falters as Trump Wins US Election",
    "Republican Surge: Class, Race, and Age Factors in Trump's US Presidential Victory",
    "Democratic Divides: US Election Results Expose Cracks in the Anti-Trump Alliance",
    "US Election 2024: Kamala Harris Struggles Amidst Shifts in American Voter Base",
    "The Coalition Cracks: Trump's Comeback and the Fissures in Democratic Support",
    "US Presidential Election Aftermath: Examining the Democratic Coalition's Vulnerabilities",
    "The New Political Landscape: Trump Capitalizes on Shifts in Class, Race, and Age",
    "Kamala Harris' Struggles: Understanding the Cracks in the Anti-Trump Coalition",
    "The Evolving American Voter Base: Insights from the 2024 US Presidential Election"
]


# Compute the embeddings for the best title and the title proposals
best_title_embedding = model.encode(best_title, convert_to_tensor=True)
title_proposals_embeddings = model.encode(title_proposals, convert_to_tensor=True)

# Compute the cosine similarities between the best title and the title proposals
cosine_scores = util.cos_sim(best_title_embedding, title_proposals_embeddings)

# Sort the title proposals by the highest cosine similarity score with the best title
sorted_title_proposals = sorted(zip(title_proposals, cosine_scores[0]), key=lambda x: x[1], reverse=True)


print('\n--- result_1: sorted title proposals')
# Print the sorted title proposals
for title, score in sorted_title_proposals:
    print(f"Title: {title} | Score: {score:.4f}")

# Filter and print the sorted title proposals where the score is >= 0.5000
filtered_title_proposals = [(title, score) for title, score in sorted_title_proposals if score >= 0.5000]

print('\n--- result_2: sorted title proposals where score is >= 0.5000')
for title, score in filtered_title_proposals:
    print(f"Title: {title} | Score: {score:.4f}")









