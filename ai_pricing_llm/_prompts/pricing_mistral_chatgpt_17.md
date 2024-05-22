
# pricing_mistral_chatgpt_17.md

## prompt_1
As an advanced programmer in Streamlit, make a cost estimation for input and output for a model according to what the user and comment on every single line.


Here are the information for the script in streamlit: 

Part_1 : Select a model
For the moment, there are several models in the dropdown "Models": "mistral-small, mistral-medium, mistral-large".


Part_2 : Price for one token for input and output
The prices per 1 Million tokens is given below in euros: 

For mistral-small
Input price = 0.9€ /1M tokens 
Output price = 2.8€ /1M tokens

For mistral-medium
Input price = 2.5€ /1M tokens 
Output price = 7.5€ /1M tokens

For mistral-large
Input price = 3.8€ /1M tokens   
Output price = 11.3€ /1M tokens


Then, give an estimation the input price for one token and give the output price for one token.


Part_3 : Total of tokens regarding the volume
The amount of characters per content goes from "500, 1000, 1500, 2000".
The amount of content goes from: "500, 1000, 2500, 5000, 75000, 10000, 15000, 20000, 50000".

Then, give an estimation for the number of Tokens both for Input and Output according to the amount of characters per content and the volume of content.

Part_4 : Global estimation costs
Make a pandas CVS for all combinations possible with proper column names.

According to the Input price and the Output price for each model, give an estimation in column for every combination.




## ChatGPT_1

Sure, let's break down the script into parts and comment on each line.

```python
import streamlit as st
import pandas as pd

# Part 1: Select a model
model_options = ["mistral-small", "mistral-medium", "mistral-large"]
selected_model = st.selectbox("Models", model_options)
# Here, we create a dropdown menu with model options and let the user select one.

# Part 2: Price for one token for input and output
# Define prices per 1 Million tokens for each model
prices = {
    "mistral-small": {"input": 0.9, "output": 2.8},
    "mistral-medium": {"input": 2.5, "output": 7.5},
    "mistral-large": {"input": 3.8, "output": 11.3}
}
# Get the selected model's prices
input_price = prices[selected_model]["input"] / 1000000
output_price = prices[selected_model]["output"] / 1000000
# Convert prices from per 1M tokens to per 1 token.

# Part 3: Total of tokens regarding the volume
# Define character counts per content and volume of content
character_counts = [500, 1000, 1500, 2000]
content_volumes = [500, 1000, 2500, 5000, 7500, 10000, 15000, 20000, 50000]

# Calculate number of tokens for input and output for each combination
token_estimations = []
for characters in character_counts:
    for volume in content_volumes:
        input_tokens = characters * volume
        output_tokens = volume
        token_estimations.append({"Characters": characters, "Volume": volume, "Input Tokens": input_tokens, "Output Tokens": output_tokens})

# Part 4: Global estimation costs
# Create a DataFrame for all combinations
df = pd.DataFrame(token_estimations)
# Calculate costs for input and output for each combination
df["Input Cost (€)"] = df["Input Tokens"] * input_price
df["Output Cost (€)"] = df["Output Tokens"] * output_price

# Show the DataFrame
st.dataframe(df)
# Save DataFrame to CSV
df.to_csv("estimation_costs.csv", index=False)
```

This script first allows the user to select a model from a dropdown menu. Then it calculates the input and output prices per token based on the selected model. After that, it calculates the number of tokens for input and output for each combination of character counts per content and volume of content. Finally, it creates a DataFrame with all combinations and calculates the costs for input and output for each combination, displaying the DataFrame and saving it to a CSV file.

## Mistral