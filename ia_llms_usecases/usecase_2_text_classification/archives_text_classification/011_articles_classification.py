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
conda env remove -n open_interpreter
conda env remove -n sentiment_analysis






# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt


# [path]
cd /Users/brunoflaven/Documents/02_copy/DERA_Ghislain_USECASES/text-classification/

# LAUNCH the file
python 011_articles_classification.py




Org-Classification-/blob/master/.py#L53



Source: text-classification-langchain-mixtral8x7b.ipynb

jupyter notebook 

python -m pip install gpt4all


Ho do use a prompt ollama with litellm and load a variable named llm ?

convert this code to work with ollama
llm=HuggingFaceHub(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1", 
                                        model_kwargs={"temperature":0.9,
                                                      "top_p":0.95,
                                                      "max_new_tokens": 250,
                                                      "repetition_penalty":1.1})
                                                      
 https://github.com/yuminglong318/Org-Classification-Ollama/blob/master/text_classification.py#L53

python -m pip install torch
python -m pip install torchvision 
                                                      
"""



from gpt4all import GPT4All
model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")
output = model.generate("What is the name of the largest city in France?", max_tokens=1024)
print(output)







