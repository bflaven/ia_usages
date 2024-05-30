"""
[env]
# Conda Environment
conda create --name fmm_fastapi_poc python=3.9.13
conda info --envs
source activate fmm_fastapi_poc
conda deactivate


# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n fmm_fastapi_poc

# BURN AFTER READING
conda env remove -n fmm_fastapi_poc


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
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_prompt_seo


# launch the file
python 003_grab_content.py


"""

import json

# Define the json file
SOURCE_FILE_JSON = "source_articles_flaven_fr.json"


# Open the file and read its contents
with open(SOURCE_FILE_JSON, "r") as f:
    data = f.read()


# Parse the JSON data
parsed_data = json.loads(data)


print('\n\n --- \/ CONTENT --- \n\n')
# Iterate over the data
for item in parsed_data:
    # Extract the required values
    id = item.get('id')
    link = item.get('link')
    title = item.get('title', {}).get('rendered')
    content = item.get('content', {}).get('rendered')
    excerpt = item.get('excerpt', {}).get('rendered')

    # Print the values
    print('ID:', id)
    print('Link:', link)
    print('Title:', title)
    print('Content:', content)
    print('Excerpt:', excerpt)
    print()
    
print('\n\n --- /\ CONTENT --- \n\n')

    







    





