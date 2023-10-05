
#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
# NO CONDA ENV

conda create --name tagging_entity_extraction python=3.9.13
conda info --envs
source activate tagging_entity_extraction

conda deactivate
# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > tagging_entity_extraction.txt



# to install
pip install -r tagging_entity_extraction.txt

[path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/spacy_language_subclass/

[file]
python 002_spacy_language_subclass.py

Source: https://spacy.io/usage/linguistic-features#language-subclass

"""

import spacy
from spacy.lang.en import English


class CustomEnglishDefaults(English.Defaults):
    stop_words = set(["custom", "stop", "Paris"])


@spacy.registry.languages("custom_en")
class CustomEnglish(English):
    lang = "custom_en"
    Defaults = CustomEnglishDefaults


# This now works! 🎉
nlp = spacy.blank("custom_en")

# print(nlp)

doc = nlp(u'I have flown to LA. Now I am flying to Frisco and I stop going to Paris')
for token in doc:
  print("Text :: " + token.text, "\npos_ :: " +
        token.pos_, "\ndep_ :: " + token.dep_ + "\n\n")





