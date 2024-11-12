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
python 015_ia_sentence_transformers.py

# source
https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
https://medium.com/@rahultiwari065/unlocking-the-power-of-sentence-embeddings-with-all-minilm-l6-v2-7d6589a5f0aa


"""
from sentence_transformers import SentenceTransformer, util

# Load the model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Define the best keywords and the keywords combinations
# best_keywords = ["France", "Switzerland", "rape", "murder", "immigration", "crime"]
# keywords_combinations = [
#     ["France", "Switzerland", "extradition", "murder", "rape", "student", "Paris", "illegal immigration", "crime", "femicide", "politicians", "rights groups"],
#     ["Extradition", "France", "Switzerland", "Paris", "university student", "murder", "Moroccan national", "illegal immigration", "crime", "femicide", "politics"],
#     ["Swiss Courts", "French Request", "Paris Student Murder", "Extradition", "Immigration Debate", "Crime", "Moroccan National"],
#     ["Paris Homicide", "Extradition", "French Authorities", "Moroccan National", "Switzerland", "Illegal Immigration", "Femicide"],
#     ["Paris University Student", "Rape and Murder", "Suspect", "Extradition", "France", "Switzerland", "Illegal Immigrant"],
#     ["Femicide", "Paris", "Student", "Moroccan National", "Extradition", "France", "Switzerland", "Crackdown on Crime"],
#     ["Paris Student Killer", "Extradition", "Moroccan National", "Switzerland", "France", "Crime", "Politics", "Femicide"],
#     ["French Politicians", "Paris University Student Murder", "Moroccan National", "Swiss Courts", "Extradition", "Femicide"],
#     ["Swiss Authorities", "Paris University Student Rape and Murder", "Extradition", "Moroccan National", "France", "Immigration Debate"],
#     ["Paris Homicide", "Moroccan National", "Extradition", "Switzerland", "France", "Illegal Immigration", "Femicide", "Politics"]
# ]

best_keywords = ["Republican Party", "USA 2024", "Donald Trump", "Kamala Harris", "US presidential election", "Democratic Party"]

keywords_combinations = [
    ["Republican Party", "USA 2024", "Democratic Party", "Donald Trump", "Kamala Harris", "US presidential election", "coalition", "class", "race", "age"],
    ["US Election", "Donald Trump", "Political Shifts", "Democratic Coalition", "Class", "Race", "Age", "Kamala Harris"],
    ["Anti-Trump Coalition", "Cracks", "US Election Results", "Republican Surge", "Class", "Race", "Age"],
    ["Kamala Harris", "Democratic Divides", "US Election 2024", "Political Landscape", "Trump", "Shifts"],
    ["Democratic Party", "Coalition", "US Presidential Election", "Voter Base", "Class", "Race", "Age", "Trump"],
    ["Republican Comeback", "Democratic Vulnerabilities", "Class", "Race", "Age", "Trump", "Kamala Harris"],
    ["Political Landscape", "US Election 2024", "Coalition", "Trump", "Kamala Harris", "Class", "Race", "Age"],
    ["Anti-Trump Alliance", "Cracks", "US Presidential Election", "Democratic Party", "Republican Surge", "Voter Base"],
    ["Voter Base", "Democratic Coalition", "US Election Results", "Class", "Race", "Age", "Trump"],
    ["Class", "Race", "Age", "Political Shifts", "Kamala Harris", "Trump", "Democratic Party", "US Election 2024"]
]


# Compute the embeddings for the best keywords and the keywords combinations
best_keywords_embedding = model.encode(" ".join(best_keywords), convert_to_tensor=True)
keywords_combinations_embeddings = [model.encode(" ".join(combination), convert_to_tensor=True) for combination in keywords_combinations]

# Compute the cosine similarities between the best keywords and the keywords combinations
cosine_scores = [util.cos_sim(best_keywords_embedding, combination_embedding) for combination_embedding in keywords_combinations_embeddings]

# Sort the keywords combinations by the highest cosine similarity score with the best keywords
sorted_keywords_combinations = sorted(zip(keywords_combinations, cosine_scores), key=lambda x: x[1], reverse=True)

# Print the sorted keywords combinations
for combination, score in sorted_keywords_combinations:
    print(f"Combination: {combination} | Score: {score.item():.4f}")





