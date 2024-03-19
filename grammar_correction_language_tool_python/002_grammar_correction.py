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
cd /Users/brunoflaven/Documents/02_copy/fmm_USECASES/journalist_workflow/grammar_correction/

# LAUNCH the file
python 002_grammar_correction.py



# install
python -m pip install langchain faiss-cpu
python -m pip install langchain-community
python -m pip install pandas 
python -m pip install numpy
python -m pip install matplotlib
python -m pip install plotly
python -m pip install seaborn
python -m pip install pyarrow


# source
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

from langchain.prompts.few_shot import FewShotPromptTemplate

# disable for the moment deprecated message
import warnings
warnings.filterwarnings("ignore", category=UserWarning)


"""
instructions:
- download ollama `https://ollama.ai/download`
    - ollama pull llama2
    - ollama pull mistral
- pip install langchain
"""

import langchain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser #PydanticOutputParser
# from langchain_core.pydantic_v1 import BaseModel, Field, validator

'''
Run mistral and get outputs for this large language model
'''

############################################################################################################################## 

'''loading the model'''

# SimpleSequentialChain
llm_model="mistral:latest"

# sentence = "Adobe patches holes in Acrobat Reader Adobe has patched two bugs in its Acrobat Reader application that could allow an attacker to take over a user #39;s system via a malicious PDF attached to an e-mail message."
# sentence = "Time Warner pays up Agrees to \$210M Justice Dept. deal and proposes paying an additional \$300M to end SEC probe. BY HARRY BERKOWITZ. Seeking to remove a cloud that has lingered over Time Warner for years, the media giant said yesterday "

# sentence = "Apple is looking at buying U.K. startup for $1 billion"

# sentence = "Iraq Halts Oil Exports from Main Southern Pipeline (Reuters) Reuters - Authorities have halted oil export\flows from the main pipeline in southern Iraq after\intelligence showed a rebel militia could strike\infrastructure, an oil official said on Saturday."

# F24_FR
# https://www.france24.com/fr/afrique/20240208-crise-au-s%C3%A9n%C3%A9gal-diff%C3%A9rends-avec-le-burkina-faso-le-mali-et-le-niger-la-c%C3%A9d%C3%A9ao-mise-%C3%A0-l-%C3%A9preuve

# sentence = "Réunion sous tension à la Cédéao. La Communauté ouest-africaine se réunit en urgence, jeudi 8 février, sur fond de crise politique au Sénégal et de différends importants avec les juntes au pouvoir au Burkina Faso, au Mali et au Niger.\n\n Le Conseil de médiation et de sécurité de l'organisation ouest-africaine a annoncé que les ministres des Affaires étrangères se retrouveraient à Abuja, la capitale du Nigeria, pour \"discuter des problèmes sécuritaires et politiques actuels de la région\". La présence du ministre sénégalais n'est pas confirmée pour le moment.\n\n Après le report de la présidentielle sénégalaise, la Cédéao a exhorté Dakar à respecter son calendrier électoral initial. Mais elle essuie de plus en plus de critiques qui remettent en cause son influence sur ses États membres.\n\n La réputation de l'organisation régionale vieille de près de 50 ans est en jeu, en particulier après le coup d'État au Niger en juillet 2023. La menace d'intervention militaire de la Cédéao dans ce pays semble ne plus être à l'ordre du jour, alors que le président déchu monsieur Mohamed Bazoum n'a toujours pas été rétabli dans ses fonctions et reste détenu.\n\n Le report de l'élection présidentielle sénégalaise est une \"nouvelle crise dont la Cédéao n'a pas besoin\", indique à l'AFP monsieur Djidenou Steve Kpoton, consultant politique béninois indépendant. \"Son impuissance face à la situation est évidente\"."

sentence = "Réunnion sous tension à la Cédéao. La Commmunauté ouest-africaine se réunit en urgennce, jeudi 8 février, sur fond de crise pollitique au Sénnégal et de différends importants avec les juntes au pouvoir au Burkina Faso, au Mali et au Niger. Le report de l'élection présidentielle sénégalaise soit une \"nouvelle crise dont la Cédéao n'a pas besoin\", indique à l'AFP monsieur Djidenou Steve Kpoton, consultant politique béninois indépendant. \"Son impuissance face à la situation est évidente\"."



# SYSTEM_PROMPT = "You are a smart and intelligent Named Entity Recognition (NER) system. I will provide you the definition of the entities you need to extract, the sentence from where your extract the entities and the output format with examples. Entity Definition:\n 1. PERSON: Short name or full name of a person from any geographic regions.\n  2. DATE: Any format of dates. Dates can also be in natural language.\n 3. LOC: Name of any geographic location, like cities, countries, continents, districts etc.\n 4. ORG: Any named organization, institution, company, government, or other group of people with a collective purpose or function.\n 5. CARDINAL: Numerals that do not fall under another type, such as counting numbers (one, two, three), fractions, and ordinals.\n 6. GPE: Geopolitical entities, including countries, cities, states.\n 7. MONEY: Monetary values, including currency symbols, monetary amounts, and terms related to money.8. PRODUCT: Objects, artifacts, and substances produced or refined for sale.\n 9. TIME: Time expressions, including specific times of day, durations, and time intervals.\n 10. PERCENT: Percentage expressions, including numerical values followed by the percent symbol (%).\n 11. WORK_OF_ART: Titles of artistic works, including books, songs, paintings, and other creative expressions.\n 12. QUANTITY: Measurements or counts of things that can be expressed in numbers.\n 13. NORP: Nationalities or religious or political groups.\n 14. EVENT: Named occurrences or happenings, including natural and human-made incidents.\n 15. ORDINAL: Words or expressions that denote a rank, order, or sequence.\n 16. FAC: Named facilities, installations, or structures, such as buildings, airports, highways, bridges, and stadiums.\n 17. LAW: Named documents made by people or organizations, such as laws, regulations, statutes, and legal codes.\n 18. LANGUAGE: Any named language entity, including individual languages or language families.\n\nOutput Format:\n{{'PERSON': [list of entities present], 'DATE': [list of entities present], 'LOC': [list of entities present], 'ORG': [list of entities present], 'CARDINAL': [list of entities present], 'GPE': [list of entities present], 'MONEY': [list of entities present], 'PRODUCT': [list of entities present], 'TIME': [list of entities present], 'PERCENT': [list of entities present], 'WORK_OF_ART': [list of entities present], 'QUANTITY': [list of entities present], 'NORP': [list of entities present], 'EVENT': [list of entities present], 'ORDINAL': [list of entities present], 'FAC': [list of entities present], 'LAW': [list of entities present], 'LANGUAGE': [list of entities present]}}\nIf no entities are presented in any categories keep it None\n\nExamples:\n\n1. Sentence: Mr. Jacob lives in Madrid since 12th January 2015.\n Output: {{'PERSON': ['Mr. Jacob'], 'DATE': ['12th January 2015'], 'GPE': ['Madrid']}}\n\n2. Sentence: The organization, ABC Corporation, was established in 1990.\n Output: {{'ORG': ['ABC Corporation'], 'DATE': ['1990']}}\n\n 3. Sentence: The price of the product is $50.\n Output: {{'PRODUCT': ['product'], 'MONEY': ['$50']}}\n\n 4. Sentence: She scored 90% in the exam. \n Output: {{'PERCENT': ['90%']}}\n\n 5. Sentence: The Mona Lisa is a famous work of art by Leonardo da Vinci.\n Output: {{'WORK_OF_ART': ['Mona Lisa'], 'PERSON': ['Leonardo da Vinci']}}\n\n 6. Sentence: Ten people attended the event yesterday.\n Output: {{'QUANTITY': ['Ten'], 'EVENT': ['event'], 'DATE': ['yesterday']}}\n\n 7. Sentence: The house is located at 10 Downing Street.\n Output: {{'LOC': ['10 Downing Street']}} 8. Sentence: English is spoken by many people worldwide.\n Output: {{'LANGUAGE': ['English']}}\n\n 9. Sentence: She is the first runner in the marathon.\n Output: {{'ORDINAL': ['first'], 'EVENT': ['marathon']}}\n\n 10. Sentence: The law prohibits smoking in public places.\n Output: {{'LAW': ['law'], 'NORP': ['public']}}\n\n\n\n11. Sentence: Mr. Rajeev Mishra and Sunita Roy are friends and they meet each other on 24/03/1998.\nOutput: {{'PERSON': ['Mr. Rajeev Mishra', 'Sunita Roy'], 'DATE': ['24/03/1998'], 'LOC': ['None']}}\n\n. Sentence: {sentence}""\nOutput: "

# SYSTEM_PROMPT = "You are a smart and intelligent Named Entity Recognition (NER) system. I will provide you the definition of the entities you need to extract, the sentence from where your extract the entities and the output format with examples. Entity Definition:\n 1. PERSON: Short name or full name of a person from any geographic regions.\n  2. DATE: Any format of dates. Dates can also be in natural language.\n 3. LOC: Name of any geographic location, like cities, countries, continents, districts etc.\n 4. ORG: Any named organization, institution, company, government, or other group of people with a collective purpose or function.\n 5. CARDINAL: Numerals that do not fall under another type, such as counting numbers (one, two, three), fractions, and ordinals.\n 6. GPE: Geopolitical entities, including countries, cities, states.\n 7. MONEY: Monetary values, including currency symbols, monetary amounts, and terms related to money.8. PRODUCT: Objects, artifacts, and substances produced or refined for sale.\n 9. TIME: Time expressions, including specific times of day, durations, and time intervals.\n 10. PERCENT: Percentage expressions, including numerical values followed by the percent symbol (%).\n 11. WORK_OF_ART: Titles of artistic works, including books, songs, paintings, and other creative expressions.\n 12. QUANTITY: Measurements or counts of things that can be expressed in numbers.\n 13. NORP: Nationalities or religious or political groups.\n 14. EVENT: Named occurrences or happenings, including natural and human-made incidents.\n 15. ORDINAL: Words or expressions that denote a rank, order, or sequence.\n 16. FAC: Named facilities, installations, or structures, such as buildings, airports, highways, bridges, and stadiums.\n 17. LAW: Named documents made by people or organizations, such as laws, regulations, statutes, and legal codes.\n 18. LANGUAGE: Any named language entity, including individual languages or language families.\n\nOutput Format:\n{{'PERSON': [list of entities present], 'DATE': [list of entities present], 'LOC': [list of entities present], 'ORG': [list of entities present], 'CARDINAL': [list of entities present], 'GPE': [list of entities present], 'MONEY': [list of entities present], 'PRODUCT': [list of entities present], 'TIME': [list of entities present], 'PERCENT': [list of entities present], 'WORK_OF_ART': [list of entities present], 'QUANTITY': [list of entities present], 'NORP': [list of entities present], 'EVENT': [list of entities present], 'ORDINAL': [list of entities present], 'FAC': [list of entities present], 'LAW': [list of entities present], 'LANGUAGE': [list of entities present]}}\nIf no entities are presented in any categories keep it None\n\nExamples:\n\n1. Sentence: Mr. Jacob lives in Madrid since 12th January 2015.\n Output: {{'PERSON': ['Mr. Jacob'], 'DATE': ['12th January 2015'], 'GPE': ['Madrid']}}\n\n2. Sentence: The organization, ABC Corporation, was established in 1990.\n Output: {{'ORG': ['ABC Corporation'], 'DATE': ['1990']}}\n\n 3. Sentence: The price of the product is $50.\n Output: {{'PRODUCT': ['product'], 'MONEY': ['$50']}}\n\n 4. Sentence: She scored 90% in the exam. \n Output: {{'PERCENT': ['90%']}}\n\n 5. Sentence: The Mona Lisa is a famous work of art by Leonardo da Vinci.\n Output: {{'WORK_OF_ART': ['Mona Lisa'], 'PERSON': ['Leonardo da Vinci']}}\n\n. Sentence: {sentence}""\nOutput: "


# SYSTEM_PROMPT = "Act as a highly intelligent grammar and spell-checker and proofread the given text in the field sentence. For this text ONLY fix grammar and spelling mistakes. Keep the text in FRENCH. Do not code. Return as the result in a field named \"text_corrected:\" the text corrected in in FRENCH and return in the field named \"corrections:\" in a python Dictionary. For each correction, keep with the original word in a field named \"source\"and the corrected word \"destination\" like so [\"source\":"", \"destination\":""].\t  Sentence: {sentence}""\nOutput: "


SYSTEM_PROMPT = "Act as a highly intelligent grammar and spell-checker and proofread the given text in the field sentence. For this text ONLY fix grammar and spelling mistakes and significantly improving clarity and flow. Keep the text in FRENCH. Return as the result in a field named \"text_corrected:\" the text corrected in in FRENCH and return in the field named \"corrections:\" in a python Dictionary. For each correction, keep with the original word in a field named \"source\"and the corrected word \"destination\" like so [\"source\":"", \"destination\":""].\t  Sentence: {sentence}""\nOutput: "




llm = Ollama(temperature=0.9, model=llm_model)

# prompt template 1
first_prompt = ChatPromptTemplate.from_template(SYSTEM_PROMPT)

# Chain 1
chain_one = LLMChain(llm=llm, prompt=first_prompt)


# overall_simple_chain = SimpleSequentialChain(chains=[chain_one], verbose=True)

overall_simple_chain = SimpleSequentialChain(chains=[chain_one], verbose=False)

result = overall_simple_chain.invoke(sentence)

print(result)








