# usecase_1_sentiment_analysis

- usecase_1 comments sentiment analysis (usecase_1_sentiment_analysis)

- **Source :** sentiment_analysis_reviews_0.csv, sample de commentaires (1001).
- **Objective :** Give a sentiment analysis on all of these comments.
- **Negative/positive:**  prediction via ML on the nature of the comment**
- 
## HOW-TO

You have to manage your development environment in Python I do it using anaconda see below for the commands.

Commands are commented out in python files

```bash
001_split_files.py
002_sentiment_analysis.py
003_merge_csv_files.py
```

```python
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

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt


# [path]
cd /Users/brunoflaven/Documents/02_copy/DERA_Ghislain_USECASES/dera-usecases/usecase_1_sentiment_analysis

# LAUNCH the file
python 009_sentiment_analysis.py


[install]
python -m pip install transformers
python -m pip install pyarrow
python -m pip install pandas
python -m pip install numpy
python -m pip install tensorflow
python -m pip install sentencepiece

[source]
https://huggingface.co/cmarkea/distilcamembert-base-sentiment

The dataset comprises 204,993 reviews for training and 4,999 reviews for the test from Amazon, and 235,516 and 4,729 critics from Allocine website. The dataset is labeled into five categories:


1 étoile : représente une appréciation terrible,
2 étoiles : mauvaise appréciation,
3 étoiles : appréciation neutre,
4 étoiles : bonne appréciation,
5 étoiles : excellente appréciation.

1 star: represents a terrible appreciation,
2 stars: bad appreciation,
3 stars: neutral appreciation,
4 stars: good appreciation,
5 stars: excellent appreciation.

"""
```

Harder to get it all working in a jupyter notebook but here are some things to get started in `0_notebook_sentiment _analysis.ipynb`

```bash
## to launch the jupyter notebook
# Go to path
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_llms_usecases/usecase_1_sentiment_analysis/

# In base launch the specific sentiment_analysis with this command
python -m ipykernel install --user --name=sentiment_analysis
# Activate the env sentiment_analysis
source activate sentiment_analysis
# Launch the jupyter notebook in this env  sentiment_analysis
jupyter notebook


## OTHER COMMANDS

## Create the virtual environment
conda create -n 'environment_name'

## Activate the virtual environment
conda activate 'environment_name'

## Make sure that ipykernel is installed
pip install --user ipykernel

## Add the new virtual environment to Jupyter
python -m ipykernel install --user --name='environment_name'

## To list existing Jupyter virtual environments
jupyter kernelspec list

## To list existing conda environments
conda env list

## To remove conda environment
conda env remove -n 'environment_name'

## To remove the environment from Jupyter
jupyter kernelspec uninstall 'environment_name'

```

