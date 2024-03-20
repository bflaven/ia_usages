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
python 017_grammar_correction_language_tool_python.py

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

https://www.listendata.com/2024/01/4-ways-to-correct-grammar-with-python.html#languagetool

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

# La vision intangible, universelle, des droits de l’homme que portait le garde des sceaux de François Mitterrand a imprégné jusqu’au bout ses écrits et prises de position. Robert Badiner est mort, dans la nuit du 8 au 9 février, à l’age de 95 ans.

# text = 'La vission intangible , universelle, des droits de l’homme que portait le garde des sceaux de François Mitterrand a imprégné jusqu’au bout ses écrits et prise de position. Robert Badinter ait mort, dans la nnuit du 8 au 9 février, à l’age de 95 an.'


mytext = """L’ancie garde des sceaux a aujourd’hui 88 ans, haute et mince silhouet à l’oreile un peu dur, la voi un peu moins ferme, mais la penséee toujours tranchant, et le rire facile. L’abolition de la peine de mort, avec la loi du 9 octobre 1981, fête aujourd’hui ses 35 ans et c’est, pour Robert Badinter, le combat d’une vie. Il l’a raconté dans deux livres, forts et poignants, L’Exécution (Fayard), en 1973, puis L’Abolition (Fayard), en 2000, et construit depuis patiemment sa statue, de discours en colloque, et un peu partout en Europe."""



doc = nlp(mytext)


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

def check_text(input_text):
    
    # Initialize LanguageTool instance  
    tool = language_tool_python.LanguageTool('fr-FR')  

    # Check for language errors in the input text  
    matches = tool.check(input_text)  

    # Initialize lists to store detected mistakes and their corrections  
    mistakes = []  
    corrections = []  
    start_positions = []  
    end_positions = []  

    # Iterate through the detected language errors  
    for rule in matches:  
        if len(rule.replacements) > 0:  
            start_positions.append(rule.offset)  
            end_positions.append(rule.errorLength + rule.offset) 

            mistake = input_text[rule.offset : rule.errorLength + rule.offset]

            
            # Check if the mistake is in either proper_nouns or pronouns
            if mistake in proper_nouns:
                proper_nouns.remove(mistake)
            elif mistake in pronouns:
                pronouns.remove(mistake)
            else:
                # Add mistake to the list if it's not in either proper_nouns or pronouns
                mistakes.append(mistake)
            mistakes.append(input_text[rule.offset : rule.errorLength + rule.offset])  
            corrections.append(rule.replacements[0])   

        return list(zip(mistakes,corrections))
            




print('\n--- result')
result = check_text(mytext)
print(result)


