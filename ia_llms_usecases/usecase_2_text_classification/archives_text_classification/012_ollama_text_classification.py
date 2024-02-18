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


python -m pip install transformers




# [path]
cd /Users/brunoflaven/Documents/02_copy/DERA_Ghislain_USECASES/text-classification/

# LAUNCH the file
python 008_ollama_text_classification.py


Source: text-classification-langchain-mixtral8x7b.ipynb

jupyter notebook 

python -m pip install litellm
python -m pip install transformers

Ho do use a prompt ollama with litellm and load a variable named llm ?

convert this code to work with ollama
llm=HuggingFaceHub(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1", 
                                        model_kwargs={"temperature":0.9,
                                                      "top_p":0.95,
                                                      "max_new_tokens": 250,
                                                      "repetition_penalty":1.1})
                                                      
 https://github.com/yuminglong318/Org-Classification-Ollama/blob/master/text_classification.py#L53



                                                      
"""

  

from transformers import HuggingFaceHub

news="Fédératrice et populaire, Margrethe II, reine du Danemark et dernière souveraine d'Europe en exercice, a annoncé dimanche qu’elle allait abdiquer le 14 janvier. Veuve depuis 2018, elle passera le sceptre à son fils aîné, le prince héritier Frederik, 55 ans."

template = """
Act as a highly intelligent news chatbot and classify the given news text into one of the following categories only 1. Politics 2.Sport 3.Technology 4.Entertainment 5.Business 
Do not code. Return only one word answer with only the category name that the given news text belongs to
News text: {news}

"""


# Initialize the HuggingFaceHub with the specified parameters
# hub = HuggingFaceHub(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1")

model = "meta-llama/Llama-2-7b-chat-hf"
hub = HuggingFaceHub(repo_id=model)

# Generate text using the model with specified parameters
generated_text = hub.generate(
    prompt=template,
    temperature=0.9,
    top_p=0.95,
    max_length=250,  # max_new_tokens is deprecated, use max_length instead
    repetition_penalty=1.1
)

print(generated_text)







