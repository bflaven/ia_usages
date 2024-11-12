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
python 020_ia_ollama.py

# source
https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
https://medium.com/@rahultiwari065/unlocking-the-power-of-sentence-embeddings-with-all-minilm-l6-v2-7d6589a5f0aa


"""
import ollama
from datetime import datetime
import os

prompt = """
Make 10 proposals for a similar title based on this title_model, 10 keywords based on on the keywords_model and this content_source.

- title_model
```text
  German opposition demands confidence vote next week as Scholz's coalition crumbles
```

- keywords_model
```text
"Germany", "Olaf Scholz", "CDU", "Ukraine"
```

- content_source
```text
Germany's Christian Democratic Union (CDU) opposition party has called on Chancellor Olaf Scholz to seek a vote of confidence next week after the ruling coalition fell apart Wednesday night with Scholz's shock dismissal of his finance minister. Scholz had promised to put his government to a confidence vote by January 15, 2025.
```

Just return the "Title Proposals" in a python object named title_proposals = [] without number and the "Keywords" in a python object named keywords_combinations = [] that contains a set of python object without number but with each keyword between quotes.
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
