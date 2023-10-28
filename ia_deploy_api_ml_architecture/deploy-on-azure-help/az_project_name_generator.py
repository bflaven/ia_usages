#!/usr/bin/python
# -*- coding: utf-8 -*-
#
"""



# Go to the dir
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_deploy_api_ml_architecture/deploy-on-azure-help/

python az_project_name_generator.py


"""


import random
import string

# List of random colors and common keywords
colors = ['red', 'blue', 'green', 'purple', 'orange', 'pink', 'yellow', 'brown', 'teal', 'gray']
keywords = ['smoke', 'ground', 'fox', 'apple', 'banana', 'sun', 'moon', 'star', 'sky', 'ocean']


# Generate a random application name
def generate_app_name():
    # Randomly select a color and keyword
    color = random.choice(colors)
    keyword = random.choice(keywords)
    
    # Generate a random 5-character string
    rand_chars = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
    
    # Randomly choose the first character as a number between 0 and 9
    first_char = str(random.randint(0, 9))
    
    # Combine all components to create the application name
    app_name = f"{color}{keyword}{first_char}{rand_chars}"
    
    return app_name

# Generate and print example application names
for _ in range(3):
    app_name = generate_app_name()
    print(app_name)





