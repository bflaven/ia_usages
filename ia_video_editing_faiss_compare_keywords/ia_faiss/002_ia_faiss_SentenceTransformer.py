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


# other libraries
conda install -c conda-forge sentence-transformers
python -m pip install sentence-transformers



# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_video_editing_faiss_compare_keywords/ia_faiss/


# launch the file
python 002_ia_faiss_SentenceTransformer.py

https://github.com/bflaven/ia_usages/tree/921276b19f5098e990588a7061511ae80af7eb7a/ia_spacy_llm



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
# Define the best keywords and the keywords combinations
best_keywords = ["Germany", "Olaf Scholz", "CDU", "Ukraine"]

keywords_combinations = [
["Germany", "CDU", "Olaf Scholz", "confidence vote"],
["Germany", "coalition crisis", "Scholz", "confidence vote"],
["Olaf Scholz", "Germany", "CDU", "confidence vote"],
["CDU", "Germany", "Scholz", "confidence vote"],
["Germany", "coalition", "Scholz", "confidence vote"],
["CDU", "Germany", "Scholz", "confidence vote"],
["finance minister", "Germany", "Scholz", "confidence vote"],
["dismissal", "Germany", "Scholz", "confidence vote"],
["Germany", "political crisis", "Scholz", "confidence vote"],
["coalition partner's departure", "Germany", "Scholz", "confidence vote"]
]


# Create an instance of the class and use it to analyze the titles and keywords
analyzer = TitleAndKeywordAnalyzer()
analyzer.analyze_titles(best_title, title_proposals)
analyzer.analyze_keywords(best_keywords, keywords_combinations)








    
