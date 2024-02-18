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
python 004_text_classification.py

Source: text-classification-langchain-mixtral8x7b.ipynb

jupyter notebook 

python -m pip install litellm


Ho do use a prompt ollama with litellm and load a variable named llm ?

convert this code to work with ollama
llm=HuggingFaceHub(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1", 
                                        model_kwargs={"temperature":0.9,
                                                      "top_p":0.95,
                                                      "max_new_tokens": 250,
                                                      "repetition_penalty":1.1})
                                                      
                                                      
                                                      
"""


from litellm import completion

response = completion(
            # model="ollama/llama2", 
            model="ollama/mistral:latest",
            messages = [{ "content": "Hello, how are you?","role": "user"}], 
            api_base="http://localhost:11434",
            stream=True,
)

print('\n--- result---\n')
for chunk in response: 
  print(chunk)













