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


pip install ctransformers

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_using_other_llm/


# LAUNCH the file
python basic.py


# EXPLICATIONS
https://github.com/samwit/langchain-tutorials/blob/382e8db4dc5e01fc400bee8d4146cb1a2e9c3150/ollama/basic.py




"""



from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler    

llm = Ollama(model="llama2", 
            #  callback_manager = CallbackManager([StreamingStdOutCallbackHandler()]),
            temperature=0.9,
             )

from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    input_variables=["topic"],
    template="Give me 5 interesting facts about {topic}?",
)

from langchain.chains import LLMChain
chain = LLMChain(llm=llm, 
                 prompt=prompt,
                 verbose=False)

# Run the chain only specifying the input variable.
print(chain.run("the moon"))

