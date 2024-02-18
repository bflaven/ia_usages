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

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt


# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_llms_usecases/usecase_1_sentiment_analysis/

# LAUNCH the file
python 002_sentiment_analysis.py


[install]
python -m pip install transformers
python -m pip install pyarrow
python -m pip install pandas
python -m pip install numpy
python -m pip install tensorflow
python -m pip install sentencepiece
python -m pip install torchvision 


[source]
# multilingual
https://huggingface.co/lxyuan/distilbert-base-multilingual-cased-sentiments-student

# french
https://huggingface.co/cmarkea/distilcamembert-base-sentiment


The dataset comprises 204,993 reviews for training and 4,999 reviews for the test from Amazon, and 235,516 and 4,729 critics from Allocine website. The dataset is labeled into five categories:


1 étoile : représente une appréciation terrible,
2 étoiles : mauvaise appréciation,
3 étoiles : appréciation neutre,
4 étoiles : bonne appréciation,
5 étoiles : excellente appréciation.

1 star: represents a terrible appreciation,
2 stars: bad appreciation,
3 stars: neutral appreciation,
4 stars: good appreciation,
5 stars: excellent appreciation.

"""

# TRANSFORMERS
from transformers import pipeline
import torch


# DATA
import numpy as np
import pandas as pd

# If you want to disable warnings
import warnings
warnings.filterwarnings("ignore")

##### MODEL
# Define your function distilled_student_sentiment_classifier
# FOR FRENCH
# distilled_student_sentiment_classifier = pipeline(task="text-classification",
#     model="cmarkea/distilcamembert-base-sentiment",
#     tokenizer="cmarkea/distilcamembert-base-sentiment", 
#     top_k=None )

# FOR english (multilingual)
distilled_student_sentiment_classifier = pipeline(task="text-classification",
    model="lxyuan/distilbert-base-multilingual-cased-sentiments-student", 
    tokenizer="lxyuan/distilbert-base-multilingual-cased-sentiments-student", 
    top_k=None 
    
)


##### VALUES
# CSV_SOURCE="data_source/source_quintly_commentaires_0.csv"

# sample_1
CSV_SOURCE="data_split/sentiment_analysis_reviews_sample_1.csv"
CSV_DESTINATION="data_destination/sentiment_analysis_reviews_sample_analysis_1.csv"

# sample_2
# CSV_SOURCE="data_split/sentiment_analysis_reviews_sample_2.csv"
# CSV_DESTINATION="data_destination/sentiment_analysis_reviews_sample_analysis_2.csv"

# sample_3
# CSV_SOURCE="data_split/sentiment_analysis_reviews_sample_3.csv"
# CSV_DESTINATION="data_destination/sentiment_analysis_reviews_sample_analysis_3.csv"


# etc

# Load the dataframe from CSV
df = pd.read_csv(CSV_SOURCE)

# Define lists to store labels and scores
labels = []
scores = []

# Iterate over each row in the dataframe
for index, row in df.iterrows():
    message = row['Text']
    # Call the sentiment classifier function
    result = distilled_student_sentiment_classifier (message)
    print('row_'+str(index))
    for row in result:
        print (row)
        max_score_label = max(row, key=lambda x: x['score'])
        label = max_score_label['label']
        score = max_score_label['score']
        # print(max_score_label)
        print(max_score_label['label'])
        print(max_score_label['score'])
        
        # Append label and score to respective lists
        labels.append(label)
        scores.append(score)

# Add new columns to the dataframe
df['label'] = labels
df['score'] = scores

# Export the dataframe to CSV
df.to_csv(CSV_DESTINATION, index=False)

print (f'the file {CSV_DESTINATION} has been created')
print('\n--- DONE')  # Printing a message indicating that the splitting process is done


