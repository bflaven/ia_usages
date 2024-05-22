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
python 005_reduce_api_costs.py

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

# Cf. https://storyarcadia.com/haiku-poems-about-sunsets/
# my input which contains spelling errors
user_input = '''As the sun sets on the horizen, it paints the sky with a breadtaking arry of colours. The beauty of a sunnset has inspired poets for centuries, and haiku poets are no exception. Haiku, a traditional form of Japanese poetry, is known for its simplicity and brevity. In just three lines, haiku poets capture the essence of a moment or experience. In this article, we will explore a collection of haiku poems about sunsets. These poems offer a glimpse into the beauty and serenity of a sunset, as well as the emotions and thoughts it can evoke.'''


# printing total words
print(len(user_input.split()))


prompt_template = f'''Given the input text:
user input: {user_input}

output must be in this format:
misspelled_word:corrected_word
...

output must not contain any other information than the format
'''



# Calling our function with prompt_template
results = openai_chat(prompt_template)

# printing response only
# print(results['answer'])

# printing complete results
# print(results)


# Split the 'answer' string by newline character
response = results['answer'].split("\n")

# Create a list comprehension to extract key-value pairs from each line
result = [(line.split(":")[0], line.split(":")[1]) for line in response if ":" in line]

# Initialize 'corrected_user_input' with 'user_input'
corrected_user_input = user_input

# Replace the misspelled words with the corrected words
for word, corrected_word in result:
    corrected_user_input = corrected_user_input.replace(word, corrected_word)

# Print the corrected user input
print(corrected_user_input)


