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
cd /Users/brunoflaven/Documents/02_copy/DERA_Ghislain_USECASES/dera-usecases/usecase_1_sentiment_analysis

# LAUNCH the file
python 003_merge_csv_files.py


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
import numpy as np
import pandas as pd

##### VALUES
FULL_CSV_DESTINATION='data_destination/full_sentiment_analysis_reviews_sample_analysis_1.csv'


##### STEP_1
# merging csv files 
df = pd.concat( 
    map(pd.read_csv, [
'data_destination/sentiment_analysis_reviews_sample_analysis_1.csv', 
'data_destination/sentiment_analysis_reviews_sample_analysis_1a.csv' # last file
        ]), ignore_index=True) 
print(df) 

# Export the dataframe to CSV
df.to_csv(FULL_CSV_DESTINATION, index=False)

print('\n--- STEP_1 : file generated')
print (f' the file {FULL_CSV_DESTINATION} has been generated')
print('\n--- You can uncomment the STEP_2, to check the file generated')


"""
##### STEP_2

print('\n--- STEP_2 : file checked OK')
# Check the export, but the file must be created
df = pd.read_csv(FULL_CSV_DESTINATION)
print(df)

# columns
df.columns
print(df.columns)
"""

# # check on specific columns
# columns = ['message','label', 'score']
# # columns = ['message','score']
# df_checked = pd.DataFrame(df, columns=columns)
# print(df_checked)





