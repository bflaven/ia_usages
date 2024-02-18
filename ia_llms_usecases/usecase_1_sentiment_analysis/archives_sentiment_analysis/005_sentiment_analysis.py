#!/usr/bin/python
# -*- coding: utf-8 -*-


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
cd /Users/brunoflaven/Documents/02_copy/DERA_Ghislain_USECASES/

# LAUNCH the file
python 005_sentiment_analysis.py


python -m pip install polyglot
polyglot download sentiment2.french
polyglot download sentiment2.english


python -m pip install six
python -m pip install numpy
sudo apt-get install python-numpy libicu-dev

python -m pip install polyglot
python -m pip install pyicu
python -m pip install pycld2
python -m pip install morfessor
python -m pip install textblob langdetect

python -m pip install transformers
python -m pip install 'transformers[torch]'
python -m pip install 'transformers[tf-cpu]'
python -m pip install pyarrow

See https://huggingface.co/docs/transformers/installation



To install TensorFlow 2.0
https://www.tensorflow.org/install/ 
To install PyTorch
https://pytorch.org/.


Source : https://huggingface.co/lxyuan/distilbert-base-multilingual-cased-sentiments-student?text=I+like+you.+I+love+you


Source for pandas:
https://github.com/bflaven/BlogArticlesExamples/blob/ef3add74ad1531b1bb0701424f40e440ad6f809d/streamlit-sweetviz-pandas-profiling-eda-made-easy/tedious_manual_eda/002_tedious_manual_eda.ipynb


"""

# TRANSFORMERS
from transformers import pipeline

# DATA
import numpy as np
import pandas as pd

# UserWarning: `return_all_scores` is now deprecated,  if want a similar functionality use `top_k=None` instead of `return_all_scores=True` or `top_k=1` instead of `return_all_scores=False`.




# distilled_student_sentiment_classifier = pipeline(model="lxyuan/distilbert-base-multilingual-cased-sentiments-student", return_all_scores=True )
distilled_student_sentiment_classifier = pipeline(model="lxyuan/distilbert-base-multilingual-cased-sentiments-student", top_k=None )




# english
# result = distilled_student_sentiment_classifier ("I love this movie and i would watch it again and again!")
# print(result)

# >> [[{'label': 'positive', 'score': 0.9731044769287109},
#   {'label': 'neutral', 'score': 0.016910076141357422},
#   {'label': 'negative', 'score': 0.009985478594899178}]]



# french
# result = distilled_student_sentiment_classifier ("🇧🇫🇲🇷 La Burkina Faso a obtenu la victoire de justesse face à la #Mauritanie, au stade de #Bouaké (Côte d’Ivoire), ce mardi 16 janvier.")
# print(result)



# malay
# distilled_student_sentiment_classifier("Saya suka filem ini dan saya akan menontonnya lagi dan lagi!")
# [[{'label': 'positive', 'score': 0.9760093688964844},
#   {'label': 'neutral', 'score': 0.01804516464471817},
#   {'label': 'negative', 'score': 0.005945465061813593}]]

# japanese
# distilled_student_sentiment_classifier("私はこの映画が大好きで、何度も見ます！")
# >> [[{'label': 'positive', 'score': 0.9342429041862488},
#   {'label': 'neutral', 'score': 0.040193185210227966},
#   {'label': 'negative', 'score': 0.025563929229974747}]]




# OUTPUT_3 Load a csv
# df = pd.read_csv('quintly_commentaires_1.csv')
# print(df)



# columns
# df.columns
# print(df.columns)




