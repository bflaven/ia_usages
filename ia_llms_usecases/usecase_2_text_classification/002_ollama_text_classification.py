#!/usr/bin/python
# -*- coding: utf-8 -*-

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

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_llms_usecases/usecase_2_text_classification/

# LAUNCH the file
python 002_ollama_text_classification.py



# install
python -m pip install langchain faiss-cpu
python -m pip install langchain-community
python -m pip install pandas 
python -m pip install numpy
python -m pip install matplotlib
python -m pip install plotly
python -m pip install seaborn
python -m pip install pyarrow



"""

# For CSV
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import warnings
# To save hugging face access token in environment
import os 

# to process the result
import json



# For LLM
from langchain_community.llms import Ollama

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler 
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import SimpleSequentialChain

# disable for the moment deprecated message
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

llm_model="mistral:latest"

# sample_3
FULL_CSV_SOURCE='data_split/training_data_news_sample_3.csv'
CSV_DESTINATION="data_destination/category_analysis_all_source_training_data_news_3.csv"

# etc

df = pd.read_csv(FULL_CSV_SOURCE, usecols=['text'])

# Iterate over each row in the dataframe
for index, row in df.iterrows():
    print('row_'+str(index))
    message = row['text']
    llm = Ollama(temperature=0.9, model=llm_model)    
    
    
    # V1 choice in a limited number of predefined categories
    # first_prompt = ChatPromptTemplate.from_template(
    #     "Act as a highly intelligent news chatbot and classify the given news text into one of the following categories only: France, Europe Africa, America, Asia-Pacific, Middle East, Sports, Economy, Technology, Culture, Environment. Do not code. Return only one word answer with only the category name that the given news text belongs to. In the output, return the result in a field named \"category_predicted:\" and return the comment in the field \"category_decision:\" in a python Dictionary.\t News text: {news}?"
    # ) 

    # V2 no choice let the LLM defined the category
    first_prompt = ChatPromptTemplate.from_template(
        "Act as a highly intelligent news chatbot and classify the given news text into the most adequate single category. Do not code. Return only one word answer with only the category name that the given news text belongs to. In the output, return the result in a field named \"category_predicted:\" and return the comment in the field \"category_decision:\" in a python Dictionary.\t News text: {news}?"
    ) 
    
    chain_one = LLMChain(llm=llm, prompt=first_prompt)
    overall_simple_chain = SimpleSequentialChain(chains=[chain_one], verbose=False)
    result = overall_simple_chain.invoke(message)
    result_dict = json.loads(result['output'])

    print(result_dict)

    # Create a DataFrame using pandas
    data_to_append = pd.DataFrame({
        "category_predicted": [result_dict["category_predicted"]],
        "category_decision": [result_dict["category_decision"]]
    })
    
    df.at[index, "category_predicted"] = result_dict["category_predicted"]
    df.at[index, "category_decision"] = result_dict["category_decision"]


# Export the DataFrame to a new CSV file
df.to_csv(CSV_DESTINATION)


