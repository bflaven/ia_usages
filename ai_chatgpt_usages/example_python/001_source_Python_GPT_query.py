#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
001_source_Python_GPT_query.py
source Python for GPT query  
QUERY :: In Python, write the code for a function that pick randomly one element from one of the following categories: Nature, Tech, Science, Life, Entertainment, Development, Videos, Cinema, Serial, Literature, Foreign politics, Philosophy.


[path]
cd /Users/brunoflaven/Documents/03_git/BlogArticlesExamples/ai_chatgpt_usages/example_python



[file]
python 001_source_Python_GPT_query.py

"""

# Here's an example code for a function that randomly selects one element from the given categories using the random module:

import random

def pick_category():
    categories = ['Nature', 'Tech', 'Science', 'Life', 'Entertainment', 'Development', 'Videos', 'Cinema', 'Serial', 'Literature', 'Foreign politics', 'Philosophy']
    return random.choice(categories)


# This code defines a function pick_category that creates a list of the given categories and uses the random.choice() function to randomly select and return one element from the list. You can call this function in your code to get a random category every time.





















