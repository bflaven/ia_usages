"""
[env]
# Conda Environment
conda create --name llm_integration_api_costs python=3.9.13
conda info --envs
source activate fmm_fastapi_poc
conda deactivate


# BURN AFTER READING
source activate fmm_fastapi_poc



# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n llm_integration_api_costs

# BURN AFTER READING
conda env remove -n mistral_integration


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# manual install
pip install openai
pip install mistralai
pip install langchain-mistralai
pip install openai

python -m pip install python-dotenv
python -m pip install openai

# [path]
cd /Users/brunoflaven/Documents/02_copy/fmm_USECASES/demo_seminaire_usecases/usecase_referent_seo

# launch the file
python 001_grab_content.py


"""

import requests
from bs4 import BeautifulSoup

# URL of the webpage
url = "https://www.france24.com/fr/asie-pacifique/20240525-en-inde-la-sixi%C3%A8me-%C3%A9tape-des-%C3%A9lections-g%C3%A9n%C3%A9rales-s-ouvre-avec-le-vote-des-rivaux-de-modi-%C3%A0-delhi"

# Sending a GET request to the webpage
response = requests.get(url)
response.raise_for_status()  # Raise an exception if the request was unsuccessful

# Parsing the HTML content of the webpage
soup = BeautifulSoup(response.content, 'html.parser')

# Extracting the title tag
title = soup.find('title').get_text()

# Extracting the main body of the post
article_body = soup.find('div', class_='t-content__body u-clearfix')
if article_body:
    paragraphs = article_body.find_all('p')
    article_text = '\n'.join(p.get_text() for p in paragraphs)
else:
    article_text = "Article body not found."

print("Title:", title)
print("Article Text:", article_text)





