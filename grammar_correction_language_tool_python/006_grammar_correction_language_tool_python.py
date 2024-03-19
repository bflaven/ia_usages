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
python 006_grammar_correction_language_tool_python.py

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

# nlp = spacy.load("en_core_web_sm")
# nlp = spacy.load("fr_core_news_sm")

nlp = spacy.load("fr_core_news_sm")

# PROPN, PRON


# text = "The rain in Spain falls mainly on the plain."

# TEXT WITH ERRORS
text = 'La vission intangible , universelle, des droits de l’homme que portait le garde des sceaux de Frannçois Mitterrand a imprégné jusqu’au bout ses écrits et prises de position. Robert Badinter ait mort, dans la nnuit du 8 au 9 février, à l’age de 95 ans.Le commandeur est mort. Le vieux monsieur, longue sillhouet émaciée par les années qu’un reste de vent menaçait toujours d’emporter, a longtemps marché à pas lents, entre deux colloques, dans les allées de son cher jardin du Luxembourg, qui s’ouvrait sous les fenêtres de son bel apartement de la rue Guynemer. Il y faisait une courte pose pour acheter un bout de reglisse dont il était fort gourmand et qu’on lui servait avec respect.'

doc = nlp(text)

# for token in doc:
#     print(token.text, token.lemma_, token.pos_, token.is_stop)

# Filter PROPN and PRON tokens
proper_nouns = []
pronouns = []

for token in doc:
    if token.pos_ == "PROPN":
        proper_nouns.append(token.text)
    elif token.pos_ == "PRON":
        pronouns.append(token.text)

print("Proper Nouns:", proper_nouns)
print("Pronouns:", pronouns)




# EXAMPLE_EN_1 (en-US)
"""
tool = language_tool_python.LanguageTool('en-US')
text = 'A sentence with a error in the Hitchhiker’s Guide tot he Galaxy'
corrected_text = tool.correct(text)
print('\n--- corrected_text')
print(corrected_text)
tool.close() 
"""

"""
# EXAMPLE_EN_1 (fr-FR)
# https://www.lemonde.fr/disparitions/article/2024/02/09/robert-badinter-est-mort_6215627_3382.html
tool = language_tool_python.LanguageTool('fr-FR')
text = 'La vission intangible , universelle, des droits de l’homme que portait le garde des sceaux de Frannçois Mitterrand a imprégné jusqu’au bout ses écrits et prises de position. Robert Badinter ait mort, dans la nnuit du 8 au 9 février, à l’age de 95 ans.Le commandeur est mort. Le vieux monsieur, longue sillhouet émaciée par les années qu’un reste de vent menaçait toujours d’emporter, a longtemps marché à pas lents, entre deux colloques, dans les allées de son cher jardin du Luxembourg, qui s’ouvrait sous les fenêtres de son bel apartement de la rue Guynemer. Il y faisait une courte pose pour acheter un bout de reglisse dont il était fort gourmand et qu’on lui servait avec respect.'

matches = tool.check(text)
result = len(matches)
print('\n--- errors detected')
print(result)
# print('\n--- errors detailed')
# print(matches)

my_mistakes = []
my_corrections = []
start_positions = []
end_positions = []
 
for rules in matches:
    if len(rules.replacements)>0:
        start_positions.append(rules.offset)
        end_positions.append(rules.errorLength+rules.offset)
        my_mistakes.append(text[rules.offset:rules.errorLength+rules.offset])
        my_corrections.append(rules.replacements[0])

print('\n--- result for corrections made')
corrections = list(zip(my_mistakes,my_corrections))
print(corrections)



corrected_text = tool.correct(text)
print('\n--- corrected_text')
print(corrected_text)
tool.close()
"""

