"""
[env]
# Conda Environment
conda create --name llm_integration_api_costs python=3.9.13
conda info --envs
source activate llm_integration_api_costs
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n llm_integration_api_costs


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# manual install
To complete

# [path]
cd /Users/brunoflaven/Documents/02_copy/fmm_USECASES/pricing_mistral_chatgpt/_ia_pricing_llm/

# launch the file
python 003_reduce_api_costs.py

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

# news heading list
news_headlines = [
    "Three arrested over Sikh activist's killing in Canada",
    "Why North Korea's latest propaganda bop is a huge TikTok hit",
    "Worst-ever job interviews: 'We had to crawl and moo'",
    "Mexico authorities find three bodies in search for tourists",
    "Brazil bridge buckles and plunges into river",
    "Remains of man thought to be hostage found in Israel",
    "Turkey halts trade with Israel over Gaza 'tragedy'",
    "Israel accused of possible war crime over killing of West Bank boy",
    "Blinken visits Kerem Shalom crossing on Gaza border",
    "Alarm in Israel at reports of possible ICC legal action over Gaza",
]

# length of news list
# len(news_headlines)

####### OUTPUT #######
# print(len(news_headlines))

formatted_news = "Given the news headlines:\n"

# looping through all news headlines and formatting them in single string
for i in range(0,len(news_headlines)):
    formatted_news += f"s{i}: {news_headlines[i]}\n"

# printing the formatted news
# print(formatted_news)



prompt_template = f'''{formatted_news}
I have these news headlines I want you to perform clustering on it.
You have to answer me in this format:
cluster1: s1,s3 ...
cluster2: s2, s6 ...
...
Do not write sentences but write it just like this starting from s0,s1,s2 ... 
Dont say anything else other than the format
'''

print(prompt_template)





