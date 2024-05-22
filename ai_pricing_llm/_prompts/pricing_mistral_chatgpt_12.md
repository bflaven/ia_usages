
# pricing_mistral_chatgpt_11.md

## prompt_1
As an advanced programmer in Streamlit, write several functions:
First, as in Word, write a function that counts the number of words in a text stored in a variable named "TEXT_SAMPLE_SUMMARY".
Then, you can use the package "llm_cost_estimation" to other several functions
First, add a function that enables a dropdown to select a model from a list of models loaded from the package "llm_cost_estimation"
Second, from this text stored in "TEXT_SAMPLE_SUMMARY", write a function that counts tokens in the text. 
Third, from this text stored in "TEXT_SAMPLE_SUMMARY", write a function that counts the number of tokens in the prompt using the text.
Fourth, from this text stored in "TEXT_SAMPLE_SUMMARY", write a function that counts the estimated number of tokens in the completion.


## ChatGPT_1




To create a Streamlit app that accomplishes all of the tasks outlined, you can use the following code snippet. This snippet does the following:

1. **Word Count**: It counts the number of words in a given text.
2. **Model Selection Dropdown**: It creates a dropdown for selecting models from the "llm_cost_estimation" package.
3. **Token Count**: It counts the tokens in the text.
4. **Prompt Token Count**: It counts the tokens in the prompt generated from the text.
5. **Completion Token Count**: It estimates the tokens in the completion.

To achieve this, you need to ensure you have installed Streamlit and the hypothetical "llm_cost_estimation" package. Note that you need to replace `'model1'`, `'model2'`, etc., with the actual models you intend to use.

```bash
# First, ensure that Streamlit is installed
!pip install streamlit

# Assuming "llm_cost_estimation" is a package with functionality to count tokens and estimate costs
!pip install llm_cost_estimation
```

Below is the Streamlit code snippet:

```python
import streamlit as st
from llm_cost_estimation import token_counter, prompt_estimator, completion_estimator  # Hypothetical package

# Define a constant for the sample text
TEXT_SAMPLE_SUMMARY = "This is a sample text. It is used to test various functions for token estimation."

# Function to count the number of words in a text
def count_words(text):
    return len(text.split())

# Create a Streamlit app
def main():
    # Display the number of words in the sample text
    st.title("LLM Token Estimation")
    st.write("Sample Text:")
    st.write(TEXT_SAMPLE_SUMMARY)
    
    word_count = count_words(TEXT_SAMPLE_SUMMARY)
    st.write("Number of words:", word_count)

    # Dropdown to select a model from a predefined list
    model_options = ['model1', 'model2', 'model3']  # Replace with actual models
    selected_model = st.selectbox("Select a model:", model_options)

    # Token count
    token_count = token_counter(TEXT_SAMPLE_SUMMARY)  # Assuming this function counts tokens in a text
    st.write("Token count:", token_count)

    # Prompt token count
    prompt_token_count = prompt_estimator(TEXT_SAMPLE_SUMMARY, selected_model)  # Assuming this function estimates prompt tokens
    st.write("Prompt token count:", prompt_token_count)

    # Completion token count
    completion_token_count = completion_estimator(TEXT_SAMPLE_SUMMARY, selected_model)  # Assuming this function estimates completion tokens
    st.write("Completion token count:", completion_token_count)

if __name__ == "__main__":
    main()
```

This code snippet demonstrates a Streamlit app that allows users to select an LLM model and provides various statistics about a text sample, such as word count, token count, prompt token count, and completion token count. The package "llm_cost_estimation" is a placeholder, so you'd need to replace it with the actual package that provides these functionalities. If you don't have such a package, you will need to create custom functions for token counting and estimation.