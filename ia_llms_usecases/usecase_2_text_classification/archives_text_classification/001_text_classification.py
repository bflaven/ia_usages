#!/usr/bin/python
# -*- coding: utf-8 -*-
#

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
cd /Users/brunoflaven/Documents/02_copy/DERA_Ghislain_USECASES/text-classification/

# LAUNCH the file
python 001_text_classification.py

Source: text-classification-langchain-mixtral8x7b.ipynb

jupyter notebook 
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import warnings
# To save hugging face access token in environment
import os 

# warnings.filterwarnings("ignore")
# %matplotlib inline

# below imports for langchain framework
# from langchain import HuggingFaceHub
# from langchain.chains import LLMChain
# from langchain.prompts import PromptTemplate

FULL_CSV_SOURCE='data/df_file_1.csv'


df = pd.read_csv(FULL_CSV_SOURCE)
# print(df)
# print(df.head())

# columns
# df.columns
# print(df.columns)

# df.info()
# print(df.info())



# updating data with 'Label' column to decode the integer labels with categorical labesl for easy inference
vis_df = df
vis_df['Label'] = vis_df['Label'].map({0:'Politics',1:'Sport',2:'Technology',3:'Entertainment',4:'Business'})

print('\n --- result_1')
print(f"The dataset contains { vis_df.Label.nunique() } unique categories")
# print(vis_df.columns)
print(vis_df.head())

print('\n --- result_2')
# filtered_rows = df[(df['Label'] == 0) | (df['Label'] == 3)]

# filtered_rows = df[(df['Label'] == 'Politics')]
# filtered_rows = df[(df['Label'] == 'Sport')]
# filtered_rows = df[(df['Label'] == 'Technology')]
# filtered_rows = df[(df['Label'] == 'Entertainment')]
# filtered_rows = df[(df['Label'] == 'Business')]
# print(filtered_rows)



