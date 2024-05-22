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
python 006_reduce_api_costs.py

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

# my input which contains spelling errors
user_input = '''The rugge9d pathw&ay winded through the th!ck f0r3st, 
obfusca+ting the way forward. The creaking of branches 
and rustling of leaves added. I wonder about the trees. Why do we wish to bear. F0rever the noise of these. More than another no!se. So close to our dwelling place?'''



####### OUTPUT #######
# printing total words
# print(len(user_input.split()))


prompt_template = f'''Given the input text:
    user input: {user_input}
    output must be in this format:
    uncleaned_word:cleaned_word
    ...
    if no replacement for uncleaned_word exist then use this format
    uncleaned_word:
    output must not contain any other information than the format
    '''

# Calling our function with prompt_template
results = openai_chat(prompt_template)

# printing response only
# print(results['answer'])

# printing complete results
# print(results)


# Split the 'response' string by newline character
response = results['answer'].split("\n")

# Display the split response to confirm contents
print("Split response:", response)

# Safely extract key-value pairs from each line, ignoring lines that don't have a ':' or are malformed
key_value_pairs = []
for line in response:
    line = line.strip()  # Remove leading/trailing whitespace
    if ':' in line:  # Ensure there's a colon
        parts = line.split(": ", 1)  # Split into at most two parts
        if len(parts) == 2:  # Ensure valid key-value structure
            key, value = parts
            key_value_pairs.append((key, value))
        else:
            print(f"Malformed line: {line}")  # Identify any malformed lines
    else:
        print(f"Invalid line (no colon): {line}")  # Catch lines without colons

# Print the extracted key-value pairs to confirm extraction
print("Extracted key-value pairs:", key_value_pairs)

# Make a copy of 'user_input' to modify
cleaned_user_input = user_input

# Replace the misspelled words with the corrected words
for word, corrected_word in key_value_pairs:
    if word in cleaned_user_input:  # Check if the word is in the input text
        cleaned_user_input = cleaned_user_input.replace(word, corrected_word)

# Print the cleaned user input to check if replacements are done
print("\n--- Cleaned user input:")
print("RESULT:", cleaned_user_input)
print("\n--- ")

# Additional diagnostics to check key-value pairs and original input
print("Original user input:", user_input)
print("Final key-value pairs:", key_value_pairs)





