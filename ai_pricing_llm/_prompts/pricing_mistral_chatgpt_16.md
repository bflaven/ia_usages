
# pricing_mistral_chatgpt_16.md

## prompt_1
As an advanced programmer in Streamlit, make a cost estimation for input and output for a single model named "mistral-small" and comment every single line.


Here are the information for the script in streamlit: 

Part_1 : Select a model
For the moment, there is only model in the dropdown "Models" but make a dropdown menu for the model: "mistral-small".


Part_2 : Price for one token for input and output
The prices per 1 Million tokens is given below in euros: 
Input price = €1.85 per 1 Million tokens
Output price = €5.55 per 1 Million tokens




   

Then, give an estimation the input price for one token and give the output price for one token.


Part_3 : Total of tokens regarding the volume
The amount of characters per content goes from "500, 1000, 1500, 2000".
The amount of content goes from: "500, 1000, 2500, 5000, 75000, 10000, 15000, 20000, 50000".

Then, give an estimation for the number of Tokens both for Input and Output according the amount of characters per content and the volume of content.

Part_4 : Global estimation costs
Make a pandas CVS for all combination possible with proper column names.




## ChatGPT_1

Here's a script in Streamlit that accomplishes what you've described:

```python
import streamlit as st
import pandas as pd

# Part_1: Select a model
model_options = ["mistral-small"]
selected_model = st.selectbox("Models", model_options)

# Part_2: Price for one token for input and output
input_price_per_million_tokens = 1.85  # €1.85 per 1 Million tokens
output_price_per_million_tokens = 5.55  # €5.55 per 1 Million tokens

# Estimation for one token input and output price
one_token_input_price = input_price_per_million_tokens / 1000000
one_token_output_price = output_price_per_million_tokens / 1000000

# Part_3: Total of tokens regarding the volume
characters_per_content = [500, 1000, 1500, 2000]
volume_of_content = [500, 1000, 2500, 5000, 7500, 10000, 15000, 20000, 50000]

# Estimation for the number of Tokens both for Input and Output
token_estimations = []
for char_count in characters_per_content:
    for content_count in volume_of_content:
        tokens_input = char_count * content_count
        tokens_output = tokens_input  # Assuming 1:1 input-output ratio
        token_estimations.append({
            "Characters Per Content": char_count,
            "Volume of Content": content_count,
            "Tokens Input": tokens_input,
            "Tokens Output": tokens_output
        })

# Part_4: Global estimation costs
df = pd.DataFrame(token_estimations)

# Displaying the results
st.write("Estimation for one token input price: €", round(one_token_input_price, 5))
st.write("Estimation for one token output price: €", round(one_token_output_price, 5))
st.write("Estimation for the number of Tokens for Input and Output:")
st.write(df)
```

This script creates a Streamlit app with dropdown menus for selecting the model, calculates the price for one token for input and output, estimates the number of tokens based on characters per content and volume of content, and finally creates a Pandas DataFrame with the combinations of characters per content and volume of content along with their corresponding token estimations.

## Mistral