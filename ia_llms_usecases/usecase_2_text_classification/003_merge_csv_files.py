#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
conda create --name news_category_analysis python=3.9.13
conda info --envs
source activate news_category_analysis
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n news_category_analysis

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# [path]
cd cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_llms_usecases/usecase_2_text_classification/

# LAUNCH the file
python 003_merge_csv_files.py



# install
python -m pip install langchain faiss-cpu
python -m pip install langchain-community
python -m pip install pandas 
python -m pip install numpy
python -m pip install matplotlib
python -m pip install plotly
python -m pip install seaborn
python -m pip install pyarrow



"""

# DATA
import numpy as np
import pandas as pd

##### VALUES
FULL_CSV_DESTINATION='data_destination/full_category_analysis_all_source_training_data_news_1.csv'

"""
##### STEP_1
# merging csv files 
df = pd.concat( 
    map(pd.read_csv, [
'data_destination/category_analysis_all_source_training_data_news_1.csv', 
'data_destination/category_analysis_all_source_training_data_news_2.csv', 
'data_destination/category_analysis_all_source_training_data_news_3.csv' # last file
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
# df.columns
# print(df.columns)



# check on specific columns
columns = ['text','category_predicted']
# columns = ['message','score']
df_checked = pd.DataFrame(df, columns=columns)
print(df_checked)





