"""
[env]
# Conda Environment
conda create --name llm_integration_api_costs python=3.9.13
conda info --envs
source activate llm_integration_api_costs
conda deactivate

# BURN AFTER READING
source activate fmm_fastapi_poc
source activate mistral_integration



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
Cf https://bobbyhadz.com/blog/python-no-module-named-openai

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ai_pricing_llm/reduce_api_costs

# launch the file
python 001_reduce_api_costs.py

# [source]
https://levelup.gitconnected.com/reduce-your-openai-api-costs-by-70-a9f123ce55a6
https://github.com/FareedKhan-dev/OpenAI-API-Cost-Reduction-Strategies

"""

# for api key
import os
from dotenv import load_dotenv

# Import the OpenAI class from the openai module
from openai import OpenAI


### 1. GET API KEY ###
# Load environment variables from the .env file
load_dotenv()

# Access the API key using os.getenv
api_key = os.getenv("OPENAI_API_KEY")


### 2. GET STUFF FROM CHATGPOT ###
# Create an instance of the OpenAI class with the provided API key
client = OpenAI(api_key=api_key)

# Set the user input to the string "Hi"
# user_input = "Hi"
user_input = "Hola"

# Create a chat completion using the OpenAI client and the user input
response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",  # Set the model to "gpt-3.5-turbo-0125"
    messages=[{"role": "user", "content": user_input}]
)

# Print the response from the chat completion
print(response.choices[0].message.content)

######## OUTPUT ########
# Hello! How can I help you today?
######## OUTPUT ########
#

# Print the usage of the response
print(response.usage)

######## OUTPUT ########
# CompletionUsage(completion_tokens=9, prompt_tokens=8, total_tokens=17)
######## OUTPUT ########