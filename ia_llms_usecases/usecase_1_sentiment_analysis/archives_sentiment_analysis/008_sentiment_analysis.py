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
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_llms_usecases/usecase_1_sentiment_analysis/archives_sentiment_analysis/


# LAUNCH the file
python 008_sentiment_analysis.py


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


python -m pip install sentencepiece
python -m pip install protobuf
python -m pip install lxml


See https://huggingface.co/docs/transformers/installation



To install TensorFlow 2.0
https://www.tensorflow.org/install/ 
To install PyTorch
https://pytorch.org/.


Source : https://huggingface.co/lxyuan/distilbert-base-multilingual-cased-sentiments-student?text=I+like+you.+I+love+you


Source for pandas:
https://github.com/bflaven/BlogArticlesExamples/blob/ef3add74ad1531b1bb0701424f40e440ad6f809d/streamlit-sweetviz-pandas-profiling-eda-made-easy/tedious_manual_eda/002_tedious_manual_eda.ipynb


"""

from transformers import pipeline

analyzer = pipeline(
    task='text-classification',
    model="cmarkea/distilcamembert-base-sentiment",
    tokenizer="cmarkea/distilcamembert-base-sentiment"
)
# sentence = "J'aime me promener en forêt même si ça me donne mal aux pieds."
sentence = "Je suis vraiment contre et il ne mérite pas ça, Halland n'a pas joué CDM mais il mérite mieux que Messi c vraiment pitoyable"
result = analyzer(
    sentence,
    top_k=None
)

# 1 star: represents a terrible appreciation,
# 2 stars: bad appreciation,
# 3 stars: neutral appreciation,
# 4 stars: good appreciation,
# 5 stars: excellent appreciation.


print(result)
# result
# [{'label': '1 star',
#   'score': 0.047529436647892},
#  {'label': '2 stars',
#   'score': 0.14150355756282806},
#  {'label': '3 stars',
#   'score': 0.3586442470550537},
#  {'label': '4 stars',
#   'score': 0.3181498646736145},
#  {'label': '5 stars',
#   'score': 0.13417290151119232}]


