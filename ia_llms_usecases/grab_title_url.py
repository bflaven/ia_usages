#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
conda create --name grab_title_url python=3.9.13
conda info --envs
source activate grab_title_url
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n grab_title_url


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

pip install beautifulsoup4
pip install requests

python -m pip install beautifulsoup4
python -m pip install requests

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_llms_usecases/

# LAUNCH the file
python grab_title_url.py

"""

import requests
from bs4 import BeautifulSoup

# List of URLs
urls = [
    "https://flaven.fr",
    "https://www.python.org",
    # Add more URLs as needed
]

# Store the HTML code
html_code = ""

# Iterate through each URL
for url in urls:
    try:
        # Fetch the HTML content of the URL
        response = requests.get(url)
        html_content = response.text

        # Parse HTML using Beautiful Soup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the title tag
        title_tag = soup.title

        # Extract text from the title tag
        title_text = title_tag.text if title_tag else "Title Not Found"

        # Print the URL and the title text
        print(f"<li>{title_text}<br><a href=\"{url}\" target=\"_blank\" rel=\"noopener\">{url}</a></li>")

        # Append to the HTML code
        html_code += f"<li>{title_text}<br><a href=\"{url}\" target=\"_blank\" rel=\"noopener\">{url}</a></li>"

    except Exception as e:
        print(f"Error processing {url}: {str(e)}")

# Print the full HTML code
print("\n--- Full HTML Code")
print("\n\n")
print(html_code)
print("\n\n")

