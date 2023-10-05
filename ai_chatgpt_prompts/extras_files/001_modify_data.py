#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
001_modify_data.py
source Python for GPT query  
QUERY :: In Python, write a function name ExtractEven that extract from only the even item from the following categories list: Nature, Tech, Science, Life, Entertainment, Development, Videos, Cinema, Serial, Literature, Foreign politics, Philosophy.
Then, write a function ExtractOdd that extract from only the odd item from the same list.


[path]
cd //Users/brunoflaven/Documents/03_git/BlogArticlesExamples/ai_chatgpt_prompts/extras_files/


[file]
python 001_modify_data.py

"""


def ExtractEven(categories):
    even_items = []
    for index, category in enumerate(categories):
        if index % 2 == 0:
            even_items.append(category)
    return even_items


def ExtractOdd(categories):
    odd_items = []
    for index, category in enumerate(categories):
        if index % 2 != 0:
            odd_items.append(category)
    return odd_items


# Example usage
categories = [
    'Nature', 'Tech', 'Science', 'Life', 'Entertainment', 'Development',
    'Videos', 'Cinema', 'Serial', 'Literature', 'Foreign politics', 'Philosophy'
]

even_categories = ExtractEven(categories)
print('Even categories:', even_categories)

odd_categories = ExtractOdd(categories)
print('Odd categories:', odd_categories)



""" OUTPUT

Even categories: ['Nature', 'Science', 'Entertainment', 'Videos', 'Serial', 'Foreign politics']
Odd categories: ['Tech', 'Life', 'Development', 'Cinema', 'Literature', 'Philosophy']

"""
























