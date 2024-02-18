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
python 026_text_classification.py

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

FULL_CSV_SOURCE='_07_published_posts_table.csv'


df = pd.read_csv(FULL_CSV_SOURCE, index_col=None)
print(df)
# print(df.head())

# columns
# df.columns
# print(df.columns)

# df.info()
# print(df.info())







