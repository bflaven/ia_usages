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
python 010_articles_classification.py




Org-Classification-/blob/master/.py#L53



Source: text-classification-langchain-mixtral8x7b.ipynb

jupyter notebook 

python -m pip install litellm


Ho do use a prompt ollama with litellm and load a variable named llm ?

convert this code to work with ollama
llm=HuggingFaceHub(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1", 
                                        model_kwargs={"temperature":0.9,
                                                      "top_p":0.95,
                                                      "max_new_tokens": 250,
                                                      "repetition_penalty":1.1})
                                                      
 https://github.com/yuminglong318/Org-Classification-Ollama/blob/master/text_classification.py#L53

python -m pip install torch
python -m pip install torchvision 
                                                      
"""
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import warnings
warnings.filterwarnings('ignore', category=UserWarning, message='TypedStorage is deprecated')


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained ("cssupport/bert-news-class").to(device)

def predict(text):
    id_to_class = {0: 'arts', 1: 'arts & culture', 2: 'black voices', 3: 'business', 4: 'college', 5: 'comedy', 6: 'crime', 7: 'culture & arts', 8: 'education', 9: 'entertainment', 10: 'environment', 11: 'fifty', 12: 'food & drink', 13: 'good news', 14: 'green', 15: 'healthy living', 16: 'home & living', 17: 'impact', 18: 'latino voices', 19: 'media', 20: 'money', 21: 'parenting', 22: 'parents', 23: 'politics', 24: 'queer voices', 25: 'religion', 26: 'science', 27: 'sports', 28: 'style', 29: 'style & beauty', 30: 'taste', 31: 'tech', 32: 'the worldpost', 33: 'travel', 34: 'u.s. news', 35: 'weddings', 36: 'weird news', 37: 'wellness', 38: 'women', 39: 'world news', 40: 'worldpost'}
    # Tokenize the input text
    inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=512, padding='max_length').to(device)
    with torch.no_grad():
        logits = model(inputs['input_ids'], inputs['attention_mask'])[0]
    # Get the predicted class index
    pred_class_idx = torch.argmax(logits, dim=1).item()
    return id_to_class[pred_class_idx]


# text ="The UK’s growing debt burden puts it on shaky ground ahead of upcoming assessments by the three main credit ratings agencies. A downgrade to its credit rating, which is a reflection of a country’s creditworthiness, could raise borrowing costs further still, although the impact may be limited."

text ="Le fardeau croissant de la dette du Royaume-Uni le place dans une situation précaire en prévision des prochaines évaluations des trois principales agences de notation de crédit. Une dégradation de la note de crédit d’un pays, qui reflète la solvabilité d’un pays, pourrait encore augmenter les coûts d’emprunt, même si l’impact pourrait être limité."

# text ="Fédératrice et populaire, Margrethe II, reine du Danemark et dernière souveraine d'Europe en exercice, a annoncé dimanche qu’elle allait abdiquer le 14 janvier. Veuve depuis 2018, elle passera le sceptre à son fils aîné, le prince héritier Frederik, 55 ans."


predicted_class = predict(text)
print(predicted_class)
#OUTPUT : business





