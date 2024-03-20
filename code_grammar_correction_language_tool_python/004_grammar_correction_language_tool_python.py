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
python 004_grammar_correction_language_tool_python.py

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

"""


import language_tool_python
tool = language_tool_python.LanguageTool('en-US')


# EXAMPLE_1
"""
You can use text with encapsuled in 3"

text = "LanguageTool offers spell and grammar checking. Just paste your text here and click the 'Check Text' button. Click the colored phrases for details on potential errors. or use this text too see an few of of the problems that LanguageTool can detecd. What do you thinks of grammar checkers? Please not that they are not perfect. Style issues get a blue marker: It's 5 P.M. in the afternoon. The weather was nice on Thursday, 27 June 2017"

# get the matches
matches = tool.check(text)
 
#DEBUG
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
     
 
     
my_new_text = list(text)
 
 
for m in range(len(start_positions)):
    for i in range(len(text)):
        my_new_text[start_positions[m]] = my_corrections[m]
        if (i>start_positions[m] and i<end_positions[m]):
            my_new_text[i]=""
     
my_new_text = "".join(my_new_text)

print('\n--- result for my_new_text')
print(my_new_text)

print('\n--- result for corrections made')
corrections = list(zip(my_mistakes,my_corrections))
print(corrections)

"""

# EXAMPLE_2
text = "Your the best but their are allso  good !"
matches = tool.check(text)
 
result = len(matches)
# 4
print('\n--- nb of possible corrections')
print(result)

# ERROR_1
# see the first mistake
print(matches[0])
# see the correction for the first mistake
print(matches[0].replacements)

# ERROR_2
# see the first mistake
print(matches[1])
# see the correction for the first mistake
print(matches[1].replacements)


# ERROR_3
# see the first mistake
print(matches[3])
# see the correction for the first mistake
print(matches[3].replacements)





