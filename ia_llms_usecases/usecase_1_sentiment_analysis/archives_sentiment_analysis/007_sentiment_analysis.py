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
python 007_sentiment_analysis.py


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
# Load the dataframe from CSV
df = pd.read_csv("quintly_commentaires_3.csv")

# Define lists to store labels and scores
labels = []
scores = []

# Iterate over each row in the dataframe
for index, row in df.iterrows():
    message = row['message']
    # print(message)
    # Call the sentiment classifier function
    result = distilled_student_sentiment_classifier (message)
    print(result)
    
    for row in result:
    	max_score_label = max(row, key=lambda x: x['score'])
    	# print(max_score_label)
    	print(max_score_label['label'])
    	print(max_score_label['score'])
    	
    	# Extract label and score
    	label = max_score_label['label']
    	score = max_score_label['score']

    	# Append label and score to respective lists
    	labels.append(label)
    	scores.append(score)

# Add new columns to the dataframe
df['label'] = labels
df['score'] = scores

# Export the dataframe to CSV
df.to_csv("quintly_commentaires_sentiment_analysis.csv", index=False)



