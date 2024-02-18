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
python 013_ollama_text_classification.py


Source: text-classification-langchain-mixtral8x7b.ipynb

jupyter notebook 

python -m pip install litellm
python -m pip install transformers
python -m pip install torchvision 
python -m pip install accelerate


Ho do use a prompt ollama with litellm and load a variable named llm ?

convert this code to work with ollama
llm=HuggingFaceHub(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1", 
                                        model_kwargs={"temperature":0.9,
                                                      "top_p":0.95,
                                                      "max_new_tokens": 250,
                                                      "repetition_penalty":1.1})
                                                      
 https://github.com/yuminglong318/Org-Classification-Ollama/blob/master/text_classification.py#L53


--- token form HF
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

Get approval from Meta
Get approval from HF
Create a read token from here : https://huggingface.co/settings/tokens
pip install transformers
execute huggingface-cli login and provide read token
Execute your code. It should work fine.
                                                      
"""

  

from transformers import AutoTokenizer
import transformers
import torch
import torchvision

# model = "meta-llama/Llama-2-7b-chat-hf"
model = "daryl149/llama-2-7b-chat-hf"

your_token="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"


tokenizer = AutoTokenizer.from_pretrained(model, token=your_token)
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    torch_dtype=torch.float16,
    device_map="auto",
)

sequences = pipeline(
    'I liked "Breaking Bad" and "Band of Brothers". Do you have any recommendations of other shows I might like?\n',
    do_sample=True,
    top_k=10,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id,
    max_length=200,
)
for seq in sequences:
    print(f"Result: {seq['generated_text']}")






