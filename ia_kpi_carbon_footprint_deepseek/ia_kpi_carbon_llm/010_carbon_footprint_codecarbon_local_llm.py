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
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_kpi_carbon_footprint_deepseek/ia_kpi_carbon_llm




# launch the file
python 010_carbon_footprint_codecarbon_local_llm.py

Codecarbon usage
https://mlco2.github.io/codecarbon/usage.html
https://asciinema.org/a/667970

https://mlco2.github.io/codecarbon/examples.html#using-the-explicit-object
https://github.com/mlco2/codecarbon/tree/master/examples


# remove model
ollama run mistral:latest
ollama rm mistral:latest

ollama run mistral-poet:latest
ollama rm mistral-poet:latest

# create model with modefile
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_kpi_carbon_footprint_deepseek/ia_kpi_carbon_llm/

ollama create mistral-poet -f Modelfile_mistral_poet


"""
import ollama
from codecarbon import EmissionsTracker

# No need to define modelfile or create the model since it's already created
# via the command line with `ollama create mistral-poet -f Modelfile_mistral_poet`

# Set up the emissions tracker
tracker = EmissionsTracker(save_to_api=True, tracking_mode="process")

# Use the existing model (that you created via command line)
model = "mistral-poet"

# Number of poems to generate
n_poems = 1

# Start tracking emissions
tracker.start()

# Generate poems
poems = []
for i in range(n_poems):
    response = ollama.chat(model=model, messages=[
        {'role': 'user', 'content': 'Write a poem for me about open source software'}
    ])
    poems.append(response['message']['content'])

# Stop tracking and get emissions data
emissions = tracker.stop()

# Print the generated poems
for i, poem in enumerate(poems):
    print(f"Poem {i+1}:\n{poem}\n")

# Print emissions data
print(f"Carbon emissions: {emissions} kg CO2eq")




        

