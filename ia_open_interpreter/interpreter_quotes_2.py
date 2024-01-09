"""

Prompt: Write me a function in Python that select randomly a unique quote among ten quotes. You can provide your own quotes on Cooking.

cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_prompt_academy_project/

python interpreter_quotes_2.py
"""

# Certainly! To achieve this, you'll first need a list of cooking-related quotes. Here's a simple Python function that selects 10 random cooking quotes from a predefined list:


import random

def get_random_cooking_quotes():
    cooking_quotes = [
        "Cooking is an art, but all art requires knowing something about the techniques and materials.",
        "The only real stumbling block is fear of failure. In cooking, you've got to have a what-the-hell attitude.",
        "Cooking is like love. It should be entered into with abandon or not at all.",
        "People who love to eat are always the best people.",
        "Cooking is about passion, so it may look slightly temperamental in a way that it's too assertive to the naked eye.",
        "Cooking is at once child's play and adult joy. And cooking done with care is an act of love.",
        "The only time to eat diet food is while you're waiting for the steak to cook.",
        "Good painting is like good cooking; it can be tasted, but not explained.",
        "Cooking is not difficult. Everyone has taste, even if they don't realize it. Even if you're not a great chef, there's nothing to stop you understanding the difference between what tastes good and what doesn't.",
        "The only thing I like better than talking about food is eating.",
        "Life is a combination of magic and pasta.",
        "In the hands of an able cook, fish can become an inexhaustible source of perpetual delight.",
    ]

    # Select 10 random cooking quotes
    selected_quotes = random.sample(cooking_quotes, 10)

    return selected_quotes

# Example usage
random_cooking_quotes = get_random_cooking_quotes()
for index, quote in enumerate(random_cooking_quotes, start=1):
    print(f"{index}. {quote}")


# Copy and paste this code into a Python script or interpreter, and it will display 10 randomly selected cooking quotes each time you run it.