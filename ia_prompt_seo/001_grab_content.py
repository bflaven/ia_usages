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
pip install beautifulsoup4

python -m pip install beautifulsoup4
python -m pip install openai

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_prompt_seo/

# launch the file
python 001_grab_content.py


"""

import requests
from bs4 import BeautifulSoup

# URL of the webpage
url = "https://flaven.fr/2024/05/unraveling-the-cost-of-ai-the-hidden-expenses-of-api-keys-and-pay-as-you-go-pricing-in-ai-based-products/"

# Fetch the webpage
response = requests.get(url)
webpage = response.content

# Parse the HTML content
soup = BeautifulSoup(webpage, "html.parser")

# Extract the title
title = soup.find('title').get_text()

# Extract the main body content
# Assuming the main content is within an article tag or a specific div
main_content = soup.find('div', {'class': 'entry-content'})  # Adjust the selector based on actual HTML structure

# Function to clean HTML tags and get text
def clean_html(html_element):
    for script in html_element(["script", "style"]):
        script.extract()  # Remove these tags
    return html_element.get_text()

# Clean the main content
cleaned_content = clean_html(main_content)

print("Title: ", title)
print("Content: ", cleaned_content)





