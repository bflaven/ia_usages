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

cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_and_the_fake_prompt_academy/
python 003_mixtral.py

Attempt made with Mixtral-8x7B-v0.1-GGUF
TheBloke/Mixtral-8x7B-v0.1-GGUF · Hugging Face 


Q: Write a Python class for a object named "Tree" with the following characteristics: Trunk, Roots, Branches, Crown. Within this Class "Tree", write four different methods (functions) for each of the four seasons: Winter, Summer, Autumn, Spring plus an extra method named Vivaldi that tells a random info among ten specific information on Tree.
A: See 003_mixtral.png

The code has been reworked with codellama:7b through ollama

"""
from typing import Any
import random

            
class Tree(object):
    
    def __init__(self, Trunk, Roots, Branches, Crown):
        self.Trunk = "The Trunk is the main part of the tree and it needs to be strong enough for all trees"
        self.Roots = "The Roots are used for holding the soil together so they need a lot more moisture than average plant."
        self.Branches = "The Branches should always be covered by leaves, but not too much or else you'll get sick of them!"
        self.Crown = "Crown is what we call your head, and it needs to stay up high so everyone can see."

    def Vivaldi(self):
        return random.choice([self.Trunk, self.Roots, self.Branches, self.Crown])

    def Summer(self):
        return "Summer season: the tree has leaves."
    
    def Autumn(self):
        return "Autumn season: the tree is producing nuts and fruits"

    def Winter(self):
        return "Winter season: the tree doesn't have any leaves"

    def Spring(self):
        return "Spring season: the tree is starting to bud."
   
# USAGE EXAMPLE 
tree = Tree(Trunk="The trunk of the tree", Roots="The roots of the tree", Branches="The branches of the tree", Crown="The crown of the tree")


print(tree.Vivaldi()) 
print(tree.Summer())  
print(tree.Autumn())  
print(tree.Winter())  
print(tree.Spring())  
