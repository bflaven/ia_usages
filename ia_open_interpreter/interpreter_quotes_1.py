"""

Prompt: Write me a function in Python that select randomly 10 quotes. Find the quotes on Cooking

cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_prompt_academy_project/

python interpreter_quotes_1.py

"""
import random

def select_quotes():
    with open('/Users/brunoflaven/Documents/01_work/blog_articles/ia_prompt_academy_project/quotes.txt', 'r') as f:
        quotes = f.readlines()
    
    return random.sample(quotes, 10)

print(select_quotes())