#!/usr/bin/python
# -*- coding: utf-8 -*-
#

"""
[env]
# Conda Environment
conda create --name langchain_ai python=3.9.13
conda info --envs
source activate langchain_ai
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n langchain_ai

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

conda install -c conda-forge langchain


# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_using_other_llm/

# LAUNCH the file
python samwit_basic.py


# EXPLICATIONS
https://github.com/samwit/langchain-tutorials/blob/382e8db4dc5e01fc400bee8d4146cb1a2e9c3150/ollama/basic.py

# FOR OLLAMA


# To run and chat with Llama 2
ollama run llama2


# list the model
ollama list

# when you are in the model you can use
>>> /?
>>> /list
>>> /set verbose

# to get out from the model
/exit



"""




from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler 
                                 
llm = Ollama(model="llama2", 
             callback_manager = CallbackManager([StreamingStdOutCallbackHandler()]))

llm("Tell me 5 facts about Roman history:")