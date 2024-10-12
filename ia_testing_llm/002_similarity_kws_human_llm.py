#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
[env]
# Conda Environment
conda create --name promptfoo python=3.9.13
conda info --envs
source activate promptfoo
conda deactivate


# BURN AFTER READING
source activate promptfoo



# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n promptfoo

# BURN AFTER READING
conda env remove -n promptfoo


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# manual install
python -m pip install pdfx
python -m pip install pypdf
python -m pip install instructor
python -m pip install spacy
python -m spacy download fr_core_news_sm
python -m spacy download fr_core_news_lg

#required 
brew install poppler
brew install tesseract-lang 

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_testing_llm/


# launch the file
python 002_similarity_kws_human_llm.py



"""

import spacy
import numpy as np

# FR
nlp = spacy.load('fr_core_news_sm')

list_ia = ["vaste remaniement ministériel", "Kaïs Saïed", "Affaires étrangères", "Défense", "secrétaires d'État", "Politique tunisienne"]
list_human = ["Tunisie", "Kaïs Saïed", "Remaniement ministériel"]

# list_ia = ["PSG", "Ligue des Champions", "Gérone", "Luis Enrique", "Tirage au sort", "Football"]
# list_human = ["Football", "Ligue des champions", "Portugal", "PSG",  "Monaco", "Real Madrid", "Juventus", "Atlético Madrid"]

print("\n --- result_1")
print("FR spacy loaded")



# Fonction pour calculer la similarité sémantique entre deux listes de mots-clés
def calculate_similarity(list1, list2, nlp):
    similarity_matrix = []
    for keyword1 in list1:
        doc1 = nlp(keyword1)
        row = []
        for keyword2 in list2:
            doc2 = nlp(keyword2)
            similarity = doc1.similarity(doc2)
            row.append(similarity)
        similarity_matrix.append(row)
    return similarity_matrix

# Calculer la similarité sémantique
similarity_matrix = calculate_similarity(list_ia, list_human, nlp)

# print("\n --- similarity_matrix")
# print(similarity_matrix)

# Fonction pour trouver les mots-clés les plus proches
def find_closest_keywords(similarity_matrix, list_ia, list_human, top_n=1):
    closest_keywords = []
    for i, row in enumerate(similarity_matrix):
        top_indices = np.argsort(row)[-top_n:][::-1]
        closest_keywords.append([(list_human[idx], row[idx]) for idx in top_indices])
    return closest_keywords

# Trouver les mots-clés les plus proches
closest_keywords = find_closest_keywords(similarity_matrix, list_ia, list_human, top_n=1)

"""
print("\n --- results_1")
# Afficher les résultats
for i, keyword in enumerate(list_ia):
    print(f"Pour le mot-clé '{keyword}' de list_ia, les mots-clés les plus proches de list_human sont :")
    for human_keyword, similarity in closest_keywords[i]:
        print(f"  - '{human_keyword}' avec une similarité de {similarity:.4f}")
"""
print("\n --- results_2")
# Afficher les résultats
# Fonction pour filtrer les mots-clés avec une similarité >= 0.50
def filter_keywords_by_similarity(similarity_matrix, list_ia, list_human, threshold=0.50):
    filtered_list_ia = []
    for i, row in enumerate(similarity_matrix):
        if any(similarity >= threshold for similarity in row):
            filtered_list_ia.append(list_ia[i])
    return filtered_list_ia

# Filtrer les mots-clés de list_ia avec une similarité >= 0.50
filtered_list_ia = filter_keywords_by_similarity(similarity_matrix, list_ia, list_human, threshold=0.50)

# Afficher la nouvelle liste list_ia filtrée
print("Nouvelle liste list_ia avec une similarité >= 0.50 :")
for keyword in filtered_list_ia:
    print(f"- {keyword}")

