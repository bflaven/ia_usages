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
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_llms_usecases/usecase_1_sentiment_analysis

# LAUNCH the file
python 001_split_files.py


[install]
python -m pip install transformers
python -m pip install pyarrow
python -m pip install pandas
python -m pip install numpy
python -m pip install tensorflow
python -m pip install sentencepiece

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

# DATA
import numpy as np  # Importing numpy library and aliasing it as np
import pandas as pd  # Importing pandas library and aliasing it as pd

##### VALUES
CSV_SOURCE="data_source/sentiment_analysis_reviews_0.csv"  # Assigning a file path to CSV_SOURCE variable

# Reading the data from CSV_SOURCE file into a pandas DataFrame
data = pd.read_csv(CSV_SOURCE)
print(data)  # Printing the DataFrame to the console

# Define the number of CSV files to split the data into
k = 50
# Define the size of each split
size = 20

# Loop to split the data into k files
for i in range(k):
    # Slicing the DataFrame to select rows for the current split
    df = data[size*i:size*(i+1)]
    # Writing the selected rows to a new CSV file with a unique name
    df.to_csv(f'data_split/sentiment_analysis_reviews_sample_{i+1}.csv', index=False)
    # Printing a message indicating that the file has been created
    print (f'the file data_split/sentiment_analysis_reviews_sample_{i+1}.csv has been created')

print('\n--- DONE')  # Printing a message indicating that the splitting process is done



