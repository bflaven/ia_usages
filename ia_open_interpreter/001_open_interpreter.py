#!/usr/bin/python
# -*- coding: utf-8 -*-
#

"""
[env]
# Conda Environment
conda create --name open_interpreter python=3.9.13
conda info --envs
source activate open_interpreter
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n open_interpreter

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# [path]

cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_and_the_fake_prompt_academy
python 001_open_interpreter.py

See https://docs.openinterpreter.com/setup#python-usage

- Installation
pip install open-interpreter


- Console or Terminal usage
interpreter


"""
from interpreter import interpreter
interpreter.chat()

# Not working
# interpreter.chat("Get the last 5 BBC news headlines.")
# interpreter.chat("Give me 5 names for Italian cooking recipes?")


