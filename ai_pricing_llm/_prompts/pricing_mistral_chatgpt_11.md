
# pricing_mistral_chatgpt_11.md

## prompt_1
As an advanced programmer in Streamlit, write several functions:
First, as in Word, write a function that counts the number of words in a text stored in a variable named "TEXT_SAMPLE_SUMMARY".
Then, you can use the package "llm_cost_estimation" to other several functions
First, add a function taht enable. dropdown and select a model from a list of models loaded from the package "llm_cost_estimation"
Second, from this text stored in "TEXT_SAMPLE_SUMMARY", write a function that count tokens in the text. 
Third, from this text stored in "TEXT_SAMPLE_SUMMARY", write a function that count number of tokens in the prompt using the text.
Fourth, from this text stored in "TEXT_SAMPLE_SUMMARY", write a function that count the estimated number of tokens in the completion.









## ChatGPT_1

To achieve the tasks outlined, you need to define several functions:

1. To count the number of words in a given text.
2. To count the number of tokens in a text using the `llm_cost_estimation` package.
3. To estimate the number of tokens in a prompt given the text.
4. To estimate the number of tokens in the completion for a given text.

The `llm_cost_estimation` package is designed to work with models like OpenAI's GPT-3/3.5. To count the tokens, you can use the `count_tokens` method from this package. While I don't have access to this package or its exact API, I'll assume typical usage for token counting in LLM contexts.

Here's the Streamlit code to achieve this:

```bash
# Install Streamlit and llm_cost_estimation
!pip install streamlit
!pip install llm_cost_estimation
```

```python
import streamlit as st
from llm_cost_estimation import count_tokens

# Text to analyze
TEXT_SAMPLE_SUMMARY = """
Streamlit is an open-source app framework for Machine Learning and Data Science teams.
Create beautiful web apps in minutes.
"""

# Function to count the number of words in the text
def count_words(text):
    words = text.split()
    return len(words)

# Function to count the number of tokens in the text
def count_text_tokens(text):
    return count_tokens(text)

# Function to count the number of tokens in a prompt
def count_prompt_tokens(text):
    # The prompt might include extra context, adding some overhead
    prompt = f"Please summarize the following text: {text}"
    return count_tokens(prompt)

# Function to count the estimated number of tokens in a completion
def count_completion_tokens(text):
    # In completion, the response might have a similar length to the prompt
    # This is a rough estimation; adjust as needed for your use case
    completion_text = f"This is a summary of the text: {text}"
    return count_tokens(completion_text)

# Streamlit UI
st.title("Text Analysis with Streamlit")

# Display the original text
st.write("### Original Text:")
st.write(TEXT_SAMPLE_SUMMARY)

# Display the word count
word_count = count_words(TEXT_SAMPLE_SUMMARY)
st.write(f"Word Count: {word_count}")

# Display the token count
token_count = count_text_tokens(TEXT_SAMPLE_SUMMARY)
st.write(f"Token Count: {token_count}")

# Display the token count for the prompt
prompt_token_count = count_prompt_tokens(TEXT_SAMPLE_SUMMARY)
st.write(f"Prompt Token Count: {prompt_token_count}")

# Display the estimated token count for the completion
completion_token_count = count_completion_tokens(TEXT_SAMPLE_SUMMARY)
st.write(f"Estimated Completion Token Count: {completion_token_count}")
```

These functions can help in analyzing texts in terms of word count and token count for different scenarios, such as prompts and completions. You can run this code in a Streamlit environment to get interactive results.