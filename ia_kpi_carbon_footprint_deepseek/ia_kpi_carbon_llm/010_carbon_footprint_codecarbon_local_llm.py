#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
[env]
# Conda Environment
conda create --name ia_debunk python=3.9.13
conda create --name carbon_footprint python=3.9.13
conda info --envs
source activate ia_debunk
source activate carbon_footprint
conda deactivate


# BURN AFTER READING
source activate ia_debunk
source activate carbon_footprint

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n ia_debunk
conda env remove -n carbon_footprint

# install packages
python -m pip install streamlit 
python -m pip install codecarbon
python -m pip install tensorflow
python -m pip install ollama


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_kpi_carbon_footprint_deepseek/ia_kpi_carbon_llm/



# launch the file
python 010_carbon_footprint_codecarbon_local_llm.py

Codecarbon usage
https://mlco2.github.io/codecarbon/usage.html
https://asciinema.org/a/667970

https://mlco2.github.io/codecarbon/examples.html#using-the-explicit-object
https://github.com/mlco2/codecarbon/tree/master/examples



"""
# PART_1
import ollama
from codecarbon import EmissionsTracker
# PART_2

# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# import pandas as pd


## PART_1
"""
modelfile='''
FROM llama2-uncensored
SYSTEM You are a poet but you like to keep it simple
PARAMETER temperature 5
'''
"""
modelfile='''
FROM deepseek-r1:latest
SYSTEM You are a poet but you like to keep it simple
PARAMETER temperature 5
'''



ollama.create(model='deepseek-r1:latest', modelfile=modelfile)
tracker = EmissionsTracker(save_to_api=True, tracking_mode="process")
model = "deepseek-r1:latest" # You need to pull the model from the CLI
n_poems = 10
# Start tracking
tracker.start()
poems = []
for i in range(n_poems):
    response = ollama.chat(model=model, messages=[{'role': 'user', 'content': 'Write a poem for me about open source software'}])
    poems.append(response['message']['content'])

emmissions = tracker.stop()


"""
## PART_2
# Define the scope of the application
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# Provide the path to your service account key
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/luis/Downloads/mozfest-d60a0151e681.json', scope)
client = gspread.authorize(creds)

# Open the Google Sheet using its title or URL
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1zGKLYhEkaD4R9l_Rhzs5blmWx608kA6BpzoTIPAO2zs/edit?usp=sharing") 
sheet = spreadsheet.get_worksheet(0)

def build_data_to_insert(poems, model):
    data = {
    'Poem': poems,
    'Description': f"Model: {model}, emissions: {emmissions / n_poems} kg/C02eq",
    "Type": "SCALE",
    "Answer Start": "0,5,BAD,GOOD"
    }
    df =pd.DataFrame(data)

    return df.astype(str).values.tolist()

# Update the sheet with DataFrame data

data_to_append = build_data_to_insert(poems, model)
sheet.append_rows(data_to_append, value_input_option='RAW')
"""

        

