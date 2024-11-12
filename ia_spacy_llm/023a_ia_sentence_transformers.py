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
python 023a_ia_sentence_transformers.py

# source
https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
https://medium.com/@rahultiwari065/unlocking-the-power-of-sentence-embeddings-with-all-minilm-l6-v2-7d6589a5f0aa


"""
from sentence_transformers import SentenceTransformer, util

# 1. The class
class TitleAndKeywordAnalyzer:
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def analyze_titles(self, best_title, title_proposals, threshold=0.5000):
        print('\n### TITLES')
        best_title_embedding = self.model.encode(best_title, convert_to_tensor=True)
        title_proposals_embeddings = self.model.encode(title_proposals, convert_to_tensor=True)
        cosine_scores = util.cos_sim(best_title_embedding, title_proposals_embeddings)
        sorted_title_proposals = sorted(zip(title_proposals, cosine_scores[0]), key=lambda x: x[1], reverse=True)
        self._print_results(sorted_title_proposals, threshold)

    def analyze_keywords(self, best_keywords, keywords_combinations, threshold=0.5000):
        print('\n### KEYWORDS')
        best_keywords_embedding = self.model.encode(" ".join(best_keywords), convert_to_tensor=True)
        keywords_combinations_embeddings = [self.model.encode(" ".join(combination), convert_to_tensor=True) for combination in keywords_combinations]
        cosine_scores = [util.cos_sim(best_keywords_embedding, combination_embedding) for combination_embedding in keywords_combinations_embeddings]
        sorted_keywords_combinations = sorted(zip(keywords_combinations, cosine_scores), key=lambda x: x[1], reverse=True)
        self._print_results(sorted_keywords_combinations, threshold)

    def _print_results(self, sorted_items, threshold):
        print('\n--- result_1: sorted items')
        for item, score in sorted_items:
            print(f"Item: {item} | Score: {score.item():.4f}")

        print(f'\n--- result_2: sorted items where score is >= {threshold}')
        filtered_items = [(item, score) for item, score in sorted_items if score.item() >= threshold]
        for item, score in filtered_items:
            print(f"Item: {item} | Score: {score.item():.4f}")

# 2. Define the variables     
title_proposals = [
"La préparation de l'UE face à une possible victoire de Trump en 2024",
"L'Europe et les États-Unis : quelle relation après une éventuelle réélection de Trump?",
"Les conséquences possibles d'une présidence secondaire de Trump pour l'Union européenne",
"Donald Trump, un nouveau mandat et l'impact sur l'UE",
"Prêt à la défense : comment l'Europe se prépare-t-elle à gérer une nouvelle présidence américaine?",
"La relation transatlantique au prisme d'une éventuelle victoire de Trump en 2024",
"Un retour de Trump à la Maison Blanche : quels risques pour l'UE?",
"L'Union européenne face aux menaces potentielles d'un second mandat Trump",
"Europe et États-Unis : comment continuer une collaboration stable après Trump?",
"Préparation de l'Union européenne à un hypothétique retour de Donald Trump en 2024"
]

keywords_combinations = [
{"Union européenne", "Présidentielle américaine 2024"},
{"Europe", "États-Unis, retour de Trump"},
{"Donald Trump", "Impact sur l'UE"},
{"Pour aller plus loin", "UE et États-Unis relations"},
{"L'été dernier", "Préparation de l'Union européenne"},
{"Union européenne", "Impact potential de Trump"},
{"Europe et États-Unis", "Collaboration stable"},
{"Donald Trump", "Nouveau mandat, implications pour l'UE"},
{"L'UE et les États-Unis", "Préparation à une deuxième présidence Trump"},
{"Présidentielle américaine 2024", "Impact sur l'Europe"}
]


best_content = "Lors de son mandat \u00e0 la Maison Blanche, Donald Trump avait retir\u00e9 les \u00c9tats-Unis de plusieurs accords internationaux et agences de l'ONU, mena\u00e7ant m\u00eame de quitter l'Otan. \u00c0 l'\u00e9poque, des hauts fonctionnaires de son \u00e9quipe agissaient comme \"garde-fous\" et l'Europe n'\u00e9tait pas en proie \u00e0 un conflit sur son territoire. Aujourd'hui, face \u00e0 la possibilit\u00e9 d'un retour au pouvoir du milliardaire, l'Europe se pr\u00e9pare activement \u00e0 se prot\u00e9ger d'une nouvelle pr\u00e9sidence du r\u00e9publicain.\n"
best_title = "\"Les garde-fous ont disparu\" : l'UE se pr\u00e9pare face \u00e0 l'hypoth\u00e8se d'une victoire de Trump"
best_keywords = ['"Union europ\\u00e9enne"', '"Pour aller plus loin"', '"\\u00c9tats-Unis"', '"Pr\\u00e9sidentielle am\\u00e9ricaine"', '"USA 2024"', '"Donald Trump"', '"D\\u00e9cryptage"', '"l\'\\u00e9t\\u00e9 dernier"']


# Create an instance of the class and use it to analyze the titles and keywords
analyzer = TitleAndKeywordAnalyzer()
analyzer.analyze_titles(best_title, title_proposals)
analyzer.analyze_keywords(best_keywords, keywords_combinations)


    
