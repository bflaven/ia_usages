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
cd /Users/brunoflaven/Documents/02_copy/DERA_Ghislain_USECASES/

# LAUNCH the file
python 006_sentiment_analysis.py


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

python -m pip install transformers
python -m pip install 'transformers[torch]'
python -m pip install 'transformers[tf-cpu]'
python -m pip install pyarrow

See https://huggingface.co/docs/transformers/installation



To install TensorFlow 2.0
https://www.tensorflow.org/install/ 
To install PyTorch
https://pytorch.org/.


Source : https://huggingface.co/lxyuan/distilbert-base-multilingual-cased-sentiments-student?text=I+like+you.+I+love+you


Source for pandas:
https://github.com/bflaven/BlogArticlesExamples/blob/ef3add74ad1531b1bb0701424f40e440ad6f809d/streamlit-sweetviz-pandas-profiling-eda-made-easy/tedious_manual_eda/002_tedious_manual_eda.ipynb


"""

# TRANSFORMERS
from transformers import pipeline

# DATA
import numpy as np
import pandas as pd


# Define your function distilled_student_sentiment_classifier
distilled_student_sentiment_classifier = pipeline(model="lxyuan/distilbert-base-multilingual-cased-sentiments-student", top_k=None )



# def distilled_student_sentiment_classifier(sentence):
#     # Your sentiment classification code goes here
#     # This is just a placeholder code to demonstrate the process
#     labels = ['positive', 'negative', 'neutral']
#     scores = [0.8, 0.1, 0.3]  # Placeholder scores

#     # Find the index of the maximum score
#     max_index = scores.index(max(scores))

#     # Extract the highest label and its corresponding score
#     highest_label = labels[max_index]
#     highest_score = scores[max_index]

#     return highest_label, highest_score

# Test the function
# sentence = "➡️ La victoire a été acquise grâce à un pénalty inscrit par Bertrand Traoré au terme d'un match poussif pour l","Ce qu'il faut retenir de cette CAN , c'est qu'il n'y a pas de petite équipe.Bravo aux Mauritaniens pour cette belle présentation.Félicitations à nous 🤗 , Étalons du Faso 🇧🇫✊❤️"
# label, score = distilled_student_sentiment_classifier(sentence)
# print("Highest Label:", label)
# print("Score:", score)




# Load the dataframe from CSV
df = pd.read_csv("quintly_commentaires_2.csv")

# Define lists to store labels and scores
labels = []
scores = []

# Iterate over each row in the dataframe
for index, row in df.iterrows():
    message = row['message']
    # print(message)
    # Call the sentiment classifier function
    result = distilled_student_sentiment_classifier (message)
    # print(result)
    
    for row in result:
    	max_score_label = max(row, key=lambda x: x['score'])
    	# print(max_score_label)
    	print(max_score_label['label'])
    	print(max_score_label['score'])


# # Add new columns to the dataframe
# df['label'] = labels
# df['score'] = scores

# # Export the dataframe to CSV
# df.to_csv("quintly_commentaires_sentiment_analysis.csv", index=False)



