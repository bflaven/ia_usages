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
python 024_ollama_text_classification.py



# install
python -m pip install langchain faiss-cpu
python -m pip install langchain-community


python -m pip install pandas 
python -m pip install numpy
python -m pip install matplotlib
python -m pip install plotly
python -m pip install seaborn
python -m pip install pyarrow


https://medium.com/scrapehero/building-qa-bot-with-ollama-local-llm-platform-c11d1e1f3035
https://github.com/amalaj7/Tesla-Insights-Ollama/blob/main/main.py

https://github.com/mneedham/LearnDataWithMark/blob/main/few-shot-prompting/notebooks/FewShotPrompting-Tutorial.ipynb

https://github.com/jocerfranquiz/stacking_llamas/blob/main/src/base.ipynb

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



"""
MODEL

Act as a highly intelligent news chatbot and classify the given news text into one of the following categories only 1. France 2. Europe 3. Afrique 4. Amériques 5. Asie-Pacifique 6. Moyen-Orient 7. Sports 8. Économie 9. Technologie 10. Culture 11. Environnement 
Do not code. Return only one word answer with only the category name that the given news text belongs to.
News text: Lancée en 2018, la sonde Parker s'approche chaque année un peu plus près du soleil. Fin 2024, elle devrait battre son propre record en ""frôlant"" notre étoile à une distance de seulement 6,1 millions de kilomètres. Objectif : en apprendre toujours plus sur la couronne et le vent solaire, ce flux de particules énergétiques qui baignent l'ensemble du système solaire.
"""


# SimpleSequentialChain
llm_model="mistral:latest"

FULL_CSV_SOURCE='_07_published_posts_table.csv'
CSV_DESTINATION="_07_published_posts_table_category_analysis.csv"
df = pd.read_csv(FULL_CSV_SOURCE, usecols=['Message'])
# Iterate over each row in the dataframe
for index, row in df.iterrows():
    print('row_'+str(index))
    message = row['Message']
    llm = Ollama(temperature=0.9, model=llm_model)    
    first_prompt = ChatPromptTemplate.from_template(
        "Act as a highly intelligent news chatbot and classify the given news text into one of the following categories only 1. France 2. Europe 3. Africa 4. America 5. Asia-Pacific 6. Middle East 7. Sports 8. Economy 9. Technology 10. Culture 11. Environment. Do not code. Return only one word answer with only the category name that the given news text belongs to. In the output, return the result in a field named \"category_predicted:\" and return the comment in the field \"category_decision:\" in a python Dictionary.\t News text: {news}?"
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
    
    new_rows_df = pd.DataFrame(data_to_append)
    



