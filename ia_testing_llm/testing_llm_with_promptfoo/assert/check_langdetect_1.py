#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
conda create --name promptfoo python=3.9.13
conda info --envs
source activate promptfoo
conda deactivate


# BURN AFTER READING
source activate promptfoo

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n promptfoo

# BURN AFTER READING
conda env remove -n promptfoo


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# manual install
pip install langdetect
python -m pip install langdetect

Check https://pypi.org/project/langdetect/
Check https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes




/Users/brunoflaven/Documents/03_git/ia_usages/ia_testing_llm/testing_llm_with_promptfoo/assert
python check_langdetect_1.py

"""

"""
from langdetect import detect, LangDetectException

result = detect("War doesn't show who's right, just who's left.")

print("\n--- RESULT")
print (result)
"""

import os
from langdetect import detect, LangDetectException

class LanguageDetector:
    def __init__(self, base_directory):
        self.base_directory = base_directory

    def detect_language(self, text):
        try:
            return detect(text)
        except LangDetectException as e:
            return f"Error detecting language: {e}"

    def process_files(self):
        for root, dirs, files in os.walk(self.base_directory):
            for file in files:
                if file == '1.txt':
                    file_path = os.path.join(root, file)
                    self.process_file(file_path)

    def process_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            result = self.detect_language(content)
            print(f"File: {file_path}")
            print(f"Detected Language: {result}")
            print("---")

if __name__ == "__main__":
    base_directory = '../articles'
    detector = LanguageDetector(base_directory)
    detector.process_files()


