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
python 002_grab_content.py


"""

import requests

# API endpoint
url = "# https://flaven.fr/wp-json/wp/v2/posts?_fields=content,author,id,excerpt,title,link&per_page=5"

# https://flaven.fr/wp-json/wp/v2/posts
# https://flaven.fr/wp-json/wp/v2/posts?_fields=author,id,excerpt,title,link
# https://flaven.fr/wp-json/wp/v2/posts?_fields=content,author,id,excerpt,title,link&per_page=5



import requests

# API endpoint
url = "https://flaven.fr/wp-json/wp/v2/posts?_fields=author,id,excerpt,title,link,content&per_page=5"

# Make the API request
response = requests.get(url)
data = response.json()

# Extract the required fields
for post in data:
    post_id = post.get("id")
    link = post.get("link")
    title = post.get("title", {}).get("rendered")
    excerpt = post.get("excerpt", {}).get("rendered")
    content = post.get("content", {}).get("rendered")
    
    # Print the extracted fields
    print(f"ID: {post_id}")
    print(f"Link: {link}")
    print(f"Title: {title}")
    print(f"Excerpt: {excerpt}")
    print(f"Content: {content}")
    print("\n" + "-"*80 + "\n")


    





