#!/usr/bin/python
# -*- coding: utf-8 -*-
#

"""


[env]
# Conda Environment
conda create --name news_category_analysis python=3.9.13
conda info --envs
source activate news_category_analysis
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n news_category_analysis

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
python 018_ollama_text_classification.py



# install
python -m pip install langchain faiss-cpu
python -m pip install langchain-community



https://medium.com/scrapehero/building-qa-bot-with-ollama-local-llm-platform-c11d1e1f3035
https://github.com/amalaj7/Tesla-Insights-Ollama/blob/main/main.py
https://github.com/mneedham/LearnDataWithMark/blob/main/few-shot-prompting/notebooks/FewShotPrompting-Tutorial.ipynb

https://github.com/jocerfranquiz/stacking_llamas/blob/main/src/base.ipynb


"""
from langchain_community.llms import Ollama

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler 
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


llm = Ollama(temperature=0.7, model="mistral:latest")


prompt = ChatPromptTemplate.from_template(
    "What is the best name to describe \
    a company that makes {product}?"
)

chain = LLMChain(llm=llm, prompt=prompt)


product = "Queen Size Sheet Set"
result = chain.invoke(product)
print(result)



