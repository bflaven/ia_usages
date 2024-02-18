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
python 003_text_classification.py

Source: text-classification-langchain-mixtral8x7b.ipynb

jupyter notebook 

python -m pip install litellm



"""


from litellm import completion

response = completion(
            # model="ollama/llama2",
            model="ollama/mistral:latest",
            messages = [{ "content": "Hello, how are you?","role": "user"}], 
            api_base="http://localhost:11434"
)

print('\n--- result---\n')
print(response)













