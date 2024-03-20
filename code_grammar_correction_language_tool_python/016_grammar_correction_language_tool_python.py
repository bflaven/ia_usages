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
python 016_grammar_correction_language_tool_python.py

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
# tool = language_tool_python.LanguageTool('fr-FR')
tool = language_check.LanguageTool('fr-FR')

# La vision intangible, universelle, des droits de l’homme que portait le garde des sceaux de François Mitterrand a imprégné jusqu’au bout ses écrits et prises de position. Robert Badiner est mort, dans la nuit du 8 au 9 février, à l’age de 95 ans.

# text = 'La vission intangible , universelle, des droits de l’homme que portait le garde des sceaux de François Mitterrand a imprégné jusqu’au bout ses écrits et prise de position. Robert Badinter ait mort, dans la nnuit du 8 au 9 février, à l’age de 95 an.'


text = """L’ancie garde des sceaux a aujourd’hui 88 ans, haute et mince ­silhouet à l’oreile un peu dur, la voix un peu moins ferme, mais la penséee toujours tranchant, et le rire facile. L’abolition de la peine de mort, avec la loi du 9 octobre 1981, fête aujourd’hui ses 35 ans et c’est, pour Robert Badinter, le combat d’une vie. Il l’a raconté dans deux livres, forts et poignants, L’Exécution (Fayard), en 1973, puis L’Abolition (Fayard), en 2000, et construit depuis patiemment sa ­statue, de discours en colloque, et un peu partout en Europe."""



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



print('\n--- errors')
errors = list(my_mistakes)
print(errors)

print('\n--- errors_changed')


# Convert all words to lowercase for case-insensitive comparison
proper_nouns_lower = [word.lower() for word in proper_nouns]
pronouns_lower = [word.lower() for word in pronouns]
errors_lower = [word.lower() for word in errors]

# Create a set of words to remove
words_to_remove = set(proper_nouns_lower + pronouns_lower)

# Remove words from errors that are in words_to_remove
corrected_errors = [word for word in errors if word.lower() not in words_to_remove]

print(corrected_errors)


print('\n--- corrections CHANGED')
corrections = list(zip(my_mistakes,corrected_errors))
print(corrections)


# corrected_text = tool.correct(text)
corrected_text = language_check.correct(text, corrections)


# print('\n--- non corrected text')
# print(text)


