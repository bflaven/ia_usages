
"""
[env]
# Conda Environment
conda create --name llm_integration_api_costs python=3.9.13
conda create --name fmm_fastapi_poc python=3.9.13
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

# manuel install
pip install mistralai
pip install langchain-mistralai
pip install python-dotenv
pip install streamlit-authenticator
pip install aiohttp
pip install ydata-profiling
pip install streamlit_pandas_profiling
pip install tiktoken
python -m pip install tiktoken
python -m pip install llm_cost_estimation
python -m pip install pandas
python -m pip install Jinja2
python -m pip install openai



# [path]
cd /Users/brunoflaven/Documents/02_copy/fmm_USECASES/pricing_mistral_chatgpt/using_nvidia_api/

# LAUNCH the file
python 003_nvidia_api_codegemma-7b.py


# source
https://build.nvidia.com/explore/discover#codegemma-7b

# required
You need to register in nvidia.com and grab an API KEY


"""

# for api key
import os
from dotenv import load_dotenv
from openai import OpenAI


### 1. GET API KEY ###
# Load environment variables from the .env file
load_dotenv()

# Access the API key using os.getenv
api_key = os.getenv("NVIDIA_API_KEY")

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = api_key
)

# user input
"""
user_input = f'''
Michael Cohen implicated his former boss Donald Trump in the hush money scheme to pay Stormy Daniels just days before the 2016 election, saying he doled out $130,000 at Trump’s direction and was promised reimbursement.

Cohen’s testimony ties together the prosecution’s allegations that Trump broke the law by falsifying business records to reimburse Cohen and conceal the hush money payment that Cohen said he made at Trump’s direction. Trump has pleaded not guilty and denies having an affair with Daniels.

Michael Cohen testifies in Trump hush money trial
Cohen and Trump mostly avoided eye contact while he testified Monday. Cohen looked directly at prosecutor Susan Hoffinger throughout most of his testimony, occasionally scanning the room or looking in the jury’s direction. Trump spent long stretches of Cohen’s questioning with his eyes closed or thumbing through a stack of news stories.

Trump’s attorneys are likely to get their chance to question Cohen on Tuesday. Trump attorney Todd Blanche is expected to try to shred Cohen’s credibility with the jury during cross-examination by painting him as a convicted perjurer who has changed his story more than once.
'''
"""
# source: https://edition.cnn.com/2024/05/13/politics/takeaways-michael-cohen-testimony-donald-trump-day-16/index.html


user_input = f'''
Apple is looking at buying U.K. startup for $1 billion
'''

# user ner tags
user_ner_tags = f'''NER TAGS: FAC, CARDINAL, NUMBER, DEMONYM, QUANTITY, TITLE, PHONE_NUMBER, NATIONAL, JOB, PERSON, LOC, NORP, TIME, CITY, EMAIL, GPE, LANGUAGE, PRODUCT, ZIP_CODE, ADDRESS, MONEY, ORDINAL, DATE, EVENT, CRIMINAL_CHARGE, STATE_OR_PROVINCE, RELIGION, DURATION, URL, WORK_OF_ART, PERCENT, CAUSE_OF_DEATH, COUNTRY, ORG, LAW, NAME, COUNTRY, RELIGION, TIME'''

# Generate the prompt template
prompt_template = f'''
Example:
I love Lamborghini, but Bugatti is even better. Although, Mercedes is a class above all. and i work in Google

Output:
cars: Lamborghini, Bugatti, Mercedes
ORG: Google

_______________________________________

Given the input text:
user input: {user_input}

perform NER detection on it.
{user_ner_tags}

'''


completion = client.chat.completions.create(
  model="google/codegemma-7b",
  messages=[{"role":"user","content":prompt_template}],
  temperature=0.5,
  top_p=1,
  max_tokens=1024,
  stream=True
)

for chunk in completion:
  if chunk.choices[0].delta.content is not None:
    print(chunk.choices[0].delta.content, end="")


