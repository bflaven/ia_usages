#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
conda create --name news_category_analysis python=3.9.13
conda info --envs
source activate news_category_analysis
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n news_category_analysis
conda env remove -n news_category_analysis
conda env remove -n sentiment_analysis



# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# [path]
cd /Users/brunoflaven/Documents/02_copy/fmm_USECASES/journalist_workflow/grammar_correction/

# LAUNCH the file
python 013_depot_grammar_correction_language_tool_python.py

# install
python -m pip install langchain faiss-cpu
python -m pip install langchain-community
python -m pip install pandas 
python -m pip install numpy
python -m pip install matplotlib
python -m pip install plotly
python -m pip install seaborn
python -m pip install pyarrow

python -m pip install happytransformer
python -m pip install language-tool-python

[source]
https://predictivehacks.com/languagetool-grammar-and-spell-checker-in-python/

https://languagetool.org/fr/
https://github.com/myint/language-check/
http://www.lingoes.net/en/translator/langcode.htm


"""

# proper_nouns = ['universelle', 'François', 'Mitterrand', 'jusqu’', 'Robert', 'Badinter']
# pronouns = ['que', '8']
# errors = ['vission', ' ,', 'Badinter', 'ait', 'nnuit']

# # Convert all words to lowercase for case-insensitive comparison
# proper_nouns_lower = [word.lower() for word in proper_nouns]
# pronouns_lower = [word.lower() for word in pronouns]
# errors_lower = [word.lower() for word in errors]

# # Create a set of words to remove
# words_to_remove = set(proper_nouns_lower + pronouns_lower)

# # Remove words from errors that are in words_to_remove
# corrected_errors = [word for word in errors if word.lower() not in words_to_remove]

# print("Corrected Errors:", corrected_errors)


proper_nouns = ['universelle', 'François', 'Mitterrand', 'jusqu’', 'Robert', 'Badinter']
pronouns = ['que', '8']

corrections = [('vission', 'vision'), (' ,', ','), ('Badinter', 'Badiner'), ('ait', 'est'), ('nnuit', 'nuit')]

# Extract words from corrections
correction_words = [correction[0] for correction in corrections]

# Find common words between correction words and proper nouns or pronouns
common_words = set(correction_words) & set(proper_nouns + pronouns)

# Filter out common words from corrections
corrected_corrections = [(word, correction[1]) for word, correction in zip(correction_words, corrections) if word not in common_words]

print("Corrected Corrections:", corrected_corrections)


