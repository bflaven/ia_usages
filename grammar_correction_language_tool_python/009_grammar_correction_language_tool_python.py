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
python 008_grammar_correction_language_tool_python_spacy_gpt.py

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

# language-tool-python
python -m pip install language-tool-python


# spacy
pip install -U pip setuptools wheel
python -m pip install -U spaCy

python -m spacy download fr_core_news_sm
python -m spacy download en_core_web_sm


[source]
https://predictivehacks.com/languagetool-grammar-and-spell-checker-in-python/

https://languagetool.org/fr/
https://github.com/myint/language-check/
http://www.lingoes.net/en/translator/langcode.htm


"""
import spacy
import language_tool_python

# Load English language model in spaCy
# ENGLISH
# nlp = spacy.load("en_core_web_sm")

# FRENCH
nlp = spacy.load("fr_core_news_sm")


# Initialize LanguageTool
# ENGLISH
# tool = language_tool_python.LanguageTool('en-EN')
# FRENCH
tool = language_tool_python.LanguageTool('fr-FR')

# Sample text
# text = "John and Mary went to the park. He enjoyed the weather."
# text = "Barack Obama and Bruni Flaven was born in Hawaii. He served as the 44th President of the United States."

# TEXT WITH ERRORS
text = 'La vission intangible , universelle, des droits de l’homme que portait le garde des sceaux de François Mitterrand a imprégné jusqu’au bout ses écrits et prises de position. Robert Badinter ait mort, dans la nnuit du 8 au 9 février, à l’age de 95 ans.Le commandeur est mort. Le vieux monsieur, longue sillhouet émaciée par les années qu’un reste de vent menaçait toujours d’emporter, a longtemps marché à pas lents, entre deux colloques, dans les allées de son cher jardin du Luxembourg, qui s’ouvrait sous les fenêtres de son bel apartement de la rue Guynemer. Il y faisait une courte pose pour acheter un bout de reglisse dont il était fort gourmand et qu’on lui servait avec respect.'



# Step 1: Extract PROPN and PRON using spaCy
doc = nlp(text)
exclude_words = set()

for token in doc:
    if token.pos_ in ['PROPN', 'PRON']:
        exclude_words.add(token.text)

print('\n--- exclude_words')
print(exclude_words)


# Step 2: Correct the text
matches = tool.check(text)
corrections = []

for match in matches:
    if match.offset != -1:
        if match.replacements:
            if all(replacement not in exclude_words for replacement in match.replacements):
                corrections.append((match.offset, match.errorlength, match.replacements[0]))

# Apply corrections
corrected_text = text
for offset, error_length, replacement in sorted(corrections, key=lambda x: x[0], reverse=True):
    corrected_text = corrected_text[:offset] + replacement + corrected_text[offset + error_length:]

print("Original Text:")
print(text)
print("\nCorrected Text:")
print(corrected_text)






