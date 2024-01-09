"""

Prompt: Write me a function in Python that select randomly a unique quote among ten quotes. You can provide your own quotes on Cooking.
Model: TheBloke/Orca-2-7B-GGUF/orca-2-7b.Q2_K.gguf through LM Studio

cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_prompt_academy_project/

python interpreter_quotes_3.py



"""

import random
quotes = ["The best way to get a good dish out of the oven is to keep the oven door closed as much as possible.",
          "Baking is all about chemistry - and that's a good thing.",
          "Cooking is all about people. The most important tools are noodles, rice and spoons.",
          "You can't make an omlet without breaking some eggs, but you can make a lot of people happy by making them.",
          "The best way to cook anything is to not mess it up too much at the start.",
          "Cooking is like love: you put in what you have and get out what you need.",
          "The secret of good cooking is simple: season everything you put in your mouth.",
          "Baking is a science, and like all sciences, it's based on experimentation.",
          "You can make the world a better place by making people happy through food."]

def pick_random_quote():
    return quotes[random.randint(0, len(quotes) - 1)]

print(pick_random_quote())


