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
python 014_grammar_correction_language_tool_python.py

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

import spacy
import language_tool_python


# EXAMPLE_EN_1 (en-US)
"""
tool = language_tool_python.LanguageTool('en-US')
text = 'A sentence with a error in the Hitchhiker’s Guide tot he Galaxy'
corrected_text = tool.correct(text)
print('\n--- corrected_text')
print(corrected_text)
tool.close() 
"""

# EXAMPLE_EN_1 (fr-FR)

# FRENCH
nlp = spacy.load("fr_core_news_sm")
tool = language_tool_python.LanguageTool('fr-FR')

# La vision intangible, universelle, des droits de l’homme que portait le garde des sceaux de François Mitterrand a imprégné jusqu’au bout ses écrits et prises de position. Robert Badiner est mort, dans la nuit du 8 au 9 février, à l’age de 95 ans.

# text = 'La vission intangible , universelle, des droits de l’homme que portait le garde des sceaux de François Mitterrand a imprégné jusqu’au bout ses écrits et prise de position. Robert Badinter ait mort, dans la nnuit du 8 au 9 février, à l’age de 95 an.'


text = 'En 2016, l’ancien garde des sceaux de François Mitterrand revenait sur l’abolition, trente-cinq ans auparavant, de la peine de mort, son grand oeuvre.\nLe vieux monsieur sort avec précaution une liasse de papiers jauni, chacuns précieusement enchassé dans une pochette de plastique. Ce sont ses souvenirs de la Révolution. Robert Badinter a tellement fréquenté les phillosophes des Lumieres qu’il donne toujours un peu l’impression d’avoir siégé à la Convention, quand il n’était pas encore au Sénat, et d’avoir longuement devisé avec Condorcet et Fabre d’Églantine dans les allées du jardin du Luxembourg. Ce sont des ombres famillières, qu’il caresse avec douceur.'



doc = nlp(text)


# Filter PROPN and PRON tokens
proper_nouns = []
pronouns = []

for token in doc:
    if token.pos_ == "PROPN":
        proper_nouns.append(token.text)
    elif token.pos_ == "PRON":
        pronouns.append(token.text)
print('\n--- PROPN and PRON')
# print("Proper Nouns:", proper_nouns)
# print("Pronouns:", pronouns)

print(proper_nouns)
print(pronouns)


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



# print('\n--- result for corrections made')
# errors = list(my_mistakes)
# print(errors)

print('\n--- corrections NOT CHANGED')
corrections = list(zip(my_mistakes,my_corrections))
print(corrections)



# Extract words from corrections
correction_words = [correction[0] for correction in corrections]

# Find common words between correction words and proper nouns or pronouns
common_words = set(correction_words) & set(proper_nouns + pronouns)

# Filter out common words from corrections
corrected_corrections = [(word, correction[1]) for word, correction in zip(correction_words, corrections) if word not in common_words]

print('\n--- corrections CHANGED')
print(corrected_corrections)


corrected_text = tool.correct(text)
print('\n--- corrected_text')
print(corrected_text)
tool.close()


