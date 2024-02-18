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
python 014_ollama_text_classification.py



# install
python -m pip install langchain faiss-cpu
python -m pip install langchain-community



https://medium.com/scrapehero/building-qa-bot-with-ollama-local-llm-platform-c11d1e1f3035
https://github.com/amalaj7/Tesla-Insights-Ollama/blob/main/main.py

https://github.com/mneedham/LearnDataWithMark/blob/main/few-shot-prompting/notebooks/FewShotPrompting-Tutorial.ipynb



"""

from langchain_community.llms import Ollama

llm = Ollama(model="mistral:latest")
result = llm.invoke("Tell me a joke")

# V1
# print(result)

# V2
# for chunks in llm.stream(result):
#     print(chunks)




# Prompt

# template = """Act as a highly intelligent news chatbot and classify the given news text into one of the following categories only 1. France 2. Europe 3. Afrique 4. Amériques 5. Asie-Pacifique 6. Moyen-Orient 7. Sports 8. Économie 9. Technologie 10. Culture 11. Environnement 
# Do not code. Return only one word answer with only the category name that the given news text belongs to. 
# {context}
# News text: {question}
# Helpful Answer:"""
# QA_CHAIN_PROMPT = PromptTemplate(
#     input_variables=["context", "question"],
#     template=template,
# )

# news="Lancée en 2018, la sonde Parker s'approche chaque année un peu plus près du soleil. Fin 2024, elle devrait battre son propre record en ""frôlant"" notre étoile à une distance de seulement 6,1 millions de kilomètres. Objectif : en apprendre toujours plus sur la couronne et le vent solaire, ce flux de particules énergétiques qui baignent l'ensemble du système solaire."

# template = """Act as a highly intelligent news chatbot and classify the given news text into one of the following categories only 1. France 2. Europe 3. Afrique 4. Amériques 5. Asie-Pacifique 6. Moyen-Orient 7. Sports 8. Économie 9. Technologie 10. Culture 11. Environnement 
# Do not code. Return only one word answer with only the category name that the given news text belongs to. 
# News text: {news}
# Helpful Answer:"""
# QA_CHAIN_PROMPT = PromptTemplate(
#     input_variables=["news"],
#     template=template,
# )



# llm = Ollama(model="mistral", callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))


# print(llm)







