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
python 001_ia_faiss_SentenceTransformer.py

https://github.com/bflaven/ia_usages/tree/921276b19f5098e990588a7061511ae80af7eb7a/ia_spacy_llm



"""

from sentence_transformers import SentenceTransformer

# Load the model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# List of sentences
sentences = ["This is an example sentence", "Each sentence is converted to an embedding"]

# Convert sentences to embeddings
embeddings = model.encode(sentences)

# Output the embeddings
print(embeddings)





    
