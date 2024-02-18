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
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_llms_usecases/usecase_2_text_classification/

# LAUNCH the file
python 001_split_files.py



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
import numpy as np  # Importing numpy library and aliasing it as np
import pandas as pd  # Importing pandas library and aliasing it as pd

##### VALUES
CSV_SOURCE="data_source/source_training_data_news_0.csv"  # Assigning a file path to CSV_SOURCE variable

# Reading the data from CSV_SOURCE file into a pandas DataFrame
data = pd.read_csv(CSV_SOURCE)
print(data)  # Printing the DataFrame to the console

# Define the number of CSV files to split the data into
k = 15
# Define the size of each split
size = 5

# Loop to split the data into k files
for i in range(k):
    # Slicing the DataFrame to select rows for the current split
    df = data[size*i:size*(i+1)]
    # Writing the selected rows to a new CSV file with a unique name
    df.to_csv(f'data_split/training_data_news_sample_{i+1}.csv', index=False)
    # Printing a message indicating that the file has been created
    print (f'the file data_split/training_data_news_sample_{i+1}.csv has been created')

print('\n--- DONE')  # Printing a message indicating that the splitting process is done



