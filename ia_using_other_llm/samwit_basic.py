#!/usr/bin/python
# -*- coding: utf-8 -*-
#

"""
[env]
# Conda Environment
conda create --name mistral_ai_streamlit python=3.9.13
conda info --envs
source activate mistral_ai_streamlit
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n mistral_ai_streamlit

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

conda install -c anaconda nltk
conda install -c pytorch pytorch
conda install -c anaconda numpy
conda install -c conda-forge gradio
conda install -c conda-forge transformers

pip install ctransformers

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_exploring_huggingface/

# LAUNCH the file
python basic.py


# EXPLICATIONS
https://github.com/samwit/langchain-tutorials/blob/382e8db4dc5e01fc400bee8d4146cb1a2e9c3150/ollama/basic.py




"""




from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler 
                                 
llm = Ollama(model="llama2", 
             callback_manager = CallbackManager([StreamingStdOutCallbackHandler()]))

llm("Tell me 5 facts about Roman history:")