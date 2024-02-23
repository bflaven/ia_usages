#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
conda create --name sentiment_analysis python=3.9.13
conda info --envs
source activate sentiment_analysis
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n sentiment_analysis
conda env remove -n faststream_kafka



# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt


# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_llms_usecases/usecase_1_sentiment_analysis/archives_sentiment_analysis/
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_llms_usecases/_archives/sentiment_analysis/archives/


# LAUNCH the file
python 002_sentiment_analysis.py


python -m pip install polyglot
polyglot download sentiment2.french
polyglot download sentiment2.english


python -m pip install six
python -m pip install numpy
sudo apt-get install python-numpy libicu-dev

python -m pip install polyglot
python -m pip install pyicu
python -m pip install pycld2
python -m pip install morfessor
python -m pip install textblob langdetect



python -m pip install PyICU

brew install intltool icu4c gettext
brew link icu4c gettext --force

from polyglot.downloader import downloader
downloader.download("embeddings2.en")
downloader.download("embeddings2.fr")

polyglot download LANG:en
polyglot download LANG:fr


"""

from polyglot.text import Text
from langdetect import detect

def analyze_sentiment(text, language):
   """
   Analyzes the sentiment of the given text in the specified language.
   """
   text = Text(text, hint_language_code=language)
   sentiment_score = text.polarity
   return sentiment_score

if __name__ == "__main__":
   # Example text in different languages
   texts = {
       "english": "I love programming!",
       # "spanish": "Me encanta programar!",
       "french": "J'adore programmer!",
       # "arabic": "أحب البرمجة!",
   }

   for language, text in texts.items():
       sentiment_score = analyze_sentiment(text, language)
       print(f"Sentiment score for {language}: {sentiment_score}")


