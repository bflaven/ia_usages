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
cd /Users/brunoflaven/Documents/03_git/ia_usages/ai_pricing_llm/reduce_api_costs


# launch the file
python 004_reduce_api_costs.py

# [source]
https://levelup.gitconnected.com/reduce-your-openai-api-costs-by-70-a9f123ce55a6
https://github.com/FareedKhan-dev/OpenAI-API-Cost-Reduction-Strategies


"""
# for api key
import os
from dotenv import load_dotenv

# Import the OpenAI class from the openai module
from openai import OpenAI



### 0. FUNCTIONS ###
def openai_chat(user_prompt):

    # Create a chat completion using the OpenAI client
    response = client.chat.completions.create(
        # Set the model to "gpt-3.5-turbo-0125"
        model="gpt-3.5-turbo-0125", 
        messages=[{"role": "user", "content": user_prompt}]
    )

    # Response from the chat completion
    answer = response.choices[0].message.content

    # Calculate the price for input tokens
    # For gpt-3.5-turbo-0125
    # Input : 0,50 US$ / 1M tokens
    
    input_price = response.usage.prompt_tokens * (0.5 / 1e6)

    # Calculate the price for output tokens
    # For gpt-3.5-turbo-0125
    # Output : 1,50 US$ / 1M tokens

    output_price = response.usage.completion_tokens * (1.5 / 1e6)

    # calculate the total price
    total_price = input_price + output_price

    # Return the answer, input price, output price, total price
    return {
        "answer": answer,
        "input_price": f"$ {input_price}",
        "output_price": f"$ {output_price}",
        "total_price": f"$ {total_price}"
    }
### 1. GET API KEY ###
# Load environment variables from the .env file
load_dotenv()

# Access the API key using os.getenv
api_key = os.getenv("OPENAI_API_KEY")


### 2. GET STUFF FROM CHATGPOT ###

# Create an instance of the OpenAI class with the provided API key
client = OpenAI(api_key=api_key)

# CHECK OUT https://www.bbc.com/news

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
    "Fear and prayers in Sudan city under siege",
    "Ryan Gosling plays one, but what makes a real stunt actor?",
    "Universities brace for disruption at graduations",
    "Tiny error in King's 21-metre Coronation scroll",
    "Bollywood meets ballots: Reel and real in Indian elections",
    "How the computer games industry is embracing AI",
    "Weekly quiz: Where did Emma Stone get her name?",

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

# print(prompt_template)


### CALL CHATGPT

# Calling our function with prompt_template
results = openai_chat(prompt_template)

# printing response only
# print(results['answer'])


# printing complete results
# print(results)

# Split the 'answer' string by newline character
responses = results['answer'].split("\n")

# Create a dictionary comprehension to extract key-value pairs from each line
clusters = {line.split(": ")[0].strip(): [i.strip() for i in line.split(": ")[1].split(",")] for line in responses if line.strip()}

# Replace the keys (s01, s02, s03, etc.) with the actual headlines from 'news_headlines'
for k, v in clusters.items():
    clusters[k] = [news_headlines[int(i[1:])] for i in v]

####### OUTPUT #######
# print clusters
print(clusters)
