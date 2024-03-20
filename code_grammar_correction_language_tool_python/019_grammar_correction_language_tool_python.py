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
python 019_grammar_correction_language_tool_python.py

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


import language_tool_python
import sys
from pathlib import Path
script_location = Path(__file__).absolute().parent


def checkGrammar(data):
    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(data)
    corrected = language_tool_python.utils.correct(data, matches)
    tool.close()
    formatAndDisplay(data, matches, corrected)


def formatAndDisplay(data='', matches=[], corrected=''):
    print('***'*30)
    print('Original Text')
    print('***'*30)
    print(data)
    print('***'*30)
    print('Grammar mistakes & Improvements')
    print('***'*30)
    for match in matches:
        incorrect_text = match.sentence.replace(
            match.matchedText, f'\033[44;33m{match.matchedText}\033[m'
        )

        rule_text = f'\033[3;31;40m{match.message}\033[m'
        suggestion = f'\033[4;32;40m{match.replacements[0]}\033[m'
        print(f"{rule_text} => {incorrect_text}")
        print(f"Suggestion : {suggestion}")

    # Corrected ----------
    print('***'*30)
    print('CORRECTED TEXT')
    print('***'*30)
    print(f'\033[3;33;40m{corrected}\033[m')
    print('---'*30)


try:
    file_location = script_location / 'demoFile.txt'
    f = open(file_location, "r")
    fileText = f.read()
    checkGrammar(fileText)

except Exception as e:
    exception_type, exception_object, exception_traceback = sys.exc_info()
    line_number = exception_traceback.tb_lineno
    print(f'line {line_number}: {exception_type} - {e}')





