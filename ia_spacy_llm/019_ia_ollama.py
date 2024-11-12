#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
[env]
# Conda Environment
conda create --name ia_spacy_llm python=3.9.13
conda info --envs
source activate ia_spacy_llm
conda deactivate


# BURN AFTER READING
source activate ia_spacy_llm

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n ia_spacy_llm

# BURN AFTER READING
conda env remove -n ia_spacy_llm


# other libraries
python -m pip install spacy 
python -m pip install spacy-llm 
python -m pip install scikit-learn
python -m pip install python-dotenv
python -m pip install langchain-openai

# spacy
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_md
python -m spacy validate

# other
python -m pip install -U sentence-transformers

# ollama
https://pypi.org/project/ollama/
python -m pip install ollama



# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_spacy_llm/


# launch the file
python 019_ia_ollama.py

# source
https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
https://medium.com/@rahultiwari065/unlocking-the-power-of-sentence-embeddings-with-all-minilm-l6-v2-7d6589a5f0aa


"""
import ollama
from datetime import datetime
import os

prompt = """
Return the "Title Proposals" in a python object named title_proposals = [] without number and the "Keywords" in a python object named keywords_combinations = [] without number but with each keyword between quotes.

Title Proposals:
1. Trump's Resurgence: US Election Reveals Cracks in Anti-Trump Coalition
2. The Fragmented Democratic Coalition: Kamala Harris Falters as Trump Wins US Election
3. Republican Surge: Class, Race, and Age Factors in Trump's US Presidential Victory
4. Democratic Divides: US Election Results Expose Cracks in the Anti-Trump Alliance
5. US Election 2024: Kamala Harris Struggles Amidst Shifts in American Voter Base
6. The Coalition Cracks: Trump's Comeback and the Fissures in Democratic Support
7. US Presidential Election Aftermath: Examining the Democratic Coalition's Vulnerabilities
8. The New Political Landscape: Trump Capitalizes on Shifts in Class, Race, and Age
9. Kamala Harris' Struggles: Understanding the Cracks in the Anti-Trump Coalition
10. The Evolving American Voter Base: Insights from the 2024 US Presidential Election

Keywords:
1. Republican Party, USA 2024, Democratic Party, Donald Trump, Kamala Harris, US presidential election, coalition, class, race, age.
2. US Election, Donald Trump, Political Shifts, Democratic Coalition, Class, Race, Age, Kamala Harris.
3. Anti-Trump Coalition, Cracks, US Election Results, Republican Surge, Class, Race, Age.
4. Kamala Harris, Democratic Divides, US Election 2024, Political Landscape, Trump, Shifts.
5. Democratic Party, Coalition, US Presidential Election, Voter Base, Class, Race, Age, Trump.
6. Republican Comeback, Democratic Vulnerabilities, Class, Race, Age, Trump, Kamala Harris.
7. Political Landscape, US Election 2024, Coalition, Trump, Kamala Harris, Class, Race, Age.
8. Anti-Trump Alliance, Cracks, US Presidential Election, Democratic Party, Republican Surge, Voter Base.
9. Voter Base, Democratic Coalition, US Election Results, Class, Race, Age, Trump.
10. Class, Race, Age, Political Shifts, Kamala Harris, Trump, Democratic Party, US Election 2024.
"""

response = ollama.chat(model='mistral:latest', messages=[
  {
    'role': 'user',
    'content': prompt,
  },
])

# Get the current date and time
now = datetime.now()

# Format the date and time as a string
datetime_str = now.strftime("%Y-%m-%d_%H-%M-%S")

# Create the filename
filename = f"ia_ollama_{datetime_str}.py"

# Create the directory if it doesn't exist
os.makedirs("ollama_output", exist_ok=True)

# Write the response to the file in the directory
with open(os.path.join("ollama_output", filename), "w") as f:
    f.write(response['message']['content'])

print(f"\n--- see the result in the python file {filename} in the directory ollama_output.")
