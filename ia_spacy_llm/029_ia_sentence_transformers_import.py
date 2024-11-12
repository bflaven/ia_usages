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
python 029_ia_sentence_transformers_import.py

# source
https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
https://medium.com/@rahultiwari065/unlocking-the-power-of-sentence-embeddings-with-all-minilm-l6-v2-7d6589a5f0aa


"""
from sentence_transformers import SentenceTransformer, util
import importlib.util

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

# 2. Load the variables from the external file

# spec = importlib.util.spec_from_file_location("ia_ollama_2024-11-08_06-47-22", "ollama_output/ia_ollama_2024-11-08_06-47-22.py")

# spec = importlib.util.spec_from_file_location("ia_ollama_2024-11-08_13-17-08", "ollama_output/ia_ollama_2024-11-08_13-17-08.py")


"""

# ia_ollama_english_2024_11_07_13_07_57.py
# ia_ollama_english_2024_11_08_06_03_32.py
# ia_ollama_english_2024_11_08_06_03_33.py
# ia_ollama_french_2024_11_08_06_47_22.py
# ia_ollama_french_2024_11_08_13_17_08.py
# ia_ollama_persian_2024_11_10_09_48_27.py
# ia_ollama_portuguese_2024_11_10_09_53_26.py
# ia_ollama_romanian_2024_11_10_09_49_49.py
# ia_ollama_russian_2024_11_10_09_52_06.py
# ia_ollama_spanish_2024_11_10_09_51_04.py
# ia_ollama_vietnamese_2024_11_10_09_42_46.py

"""

spec = importlib.util.spec_from_file_location("ia_ollama_portuguese_2024_11_10_09_53_26", "ollama_output/ia_ollama_portuguese_2024_11_10_09_53_26.py")





ia_ollama = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ia_ollama)



best_title = ia_ollama.best_title
title_proposals = ia_ollama.title_proposals
best_keywords = ia_ollama.best_keywords
keywords_combinations = ia_ollama.keywords_combinations

# Create an instance of the class and use it to analyze the titles and keywords
analyzer = TitleAndKeywordAnalyzer()
analyzer.analyze_titles(best_title, title_proposals)
analyzer.analyze_keywords(best_keywords, keywords_combinations)
    
