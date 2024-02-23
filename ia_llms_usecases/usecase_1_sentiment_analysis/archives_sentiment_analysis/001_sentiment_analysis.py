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

# LAUNCH the file
python 001_sentiment_analysis.py


python -m pip install textblob


"""

from textblob import TextBlob

def analyze_sentiment(text):
    # Create a TextBlob object
    blob = TextBlob(text)
    
    # Perform sentiment analysis
    sentiment = blob.sentiment.polarity
    
    # Define sentiment polarity categories
    if sentiment > 0:
        return 'positive'
    elif sentiment < 0:
        return 'negative'
    else:
        return 'neutral'

if __name__ == "__main__":
    # Example texts for sentiment analysis
    texts = [
        # "I love this product! It's amazing.",
        # "I hate dealing with customer service.",
        # "The weather today is okay.",
        # "Python is my favorite programming language.",
        # "🇧🇫🇲🇷 La Burkina Faso a obtenu la victoire de justesse face à la #Mauritanie, au stade de #Bouaké (Côte d’Ivoire), ce mardi 16 janvier"
        # "➡️ La victoire a été acquise grâce à un pénalty inscrit par Bertrand Traoré au terme d'un match poussif pour l","On dit la Burkina Faso ou bien le Burkina Faso?"
    ]

    # Analyze sentiment for each text
    for text in texts:
        sentiment = analyze_sentiment(text)
        print(f"Text: '{text}' --> Sentiment: {sentiment}")
