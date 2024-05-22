
# pricing_mistral_chatgpt_17.md

## prompt_1
As an advanced programmer in Streamlit, change the script so according to character_counts, it create a csv with multiple sheets where the value "character_counts" remains the same e.g first sheet is named "character_counts_500", named "character_counts_1000"... etc.

So according the average token numer per content, I have all the pricing estimation.


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
        output_tokens = input_tokens # Assuming 1:1 input-output ratio
        token_estimations.append({
            "Characters": characters, 
            "Volume": volume, 
            "Input Tokens": input_tokens, 
            "Output Tokens": output_tokens})

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



## ChatGPT_1

To modify the script to create a CSV with multiple sheets based on the `character_counts`, you can utilize the `pandas.ExcelWriter` module. Here's the updated script:

```python
import streamlit as st
import pandas as pd

# Part 1: Select a model
model_options = ["mistral-small", "mistral-medium", "mistral-large"]
selected_model = st.selectbox("Models", model_options)

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

# Part 3: Total of tokens regarding the volume
# Define character counts per content and volume of content
character_counts = [500, 1000, 1500, 2000]
content_volumes = [500, 1000, 2500, 5000, 7500, 10000, 15000, 20000, 50000]

# Calculate number of tokens for input and output for each combination
token_estimations = []
for characters in character_counts:
    for volume in content_volumes:
        input_tokens = characters * volume
        output_tokens = input_tokens # Assuming 1:1 input-output ratio
        token_estimations.append({
            "Characters": characters, 
            "Volume": volume, 
            "Input Tokens": input_tokens, 
            "Output Tokens": output_tokens})

# Part 4: Global estimation costs
# Create a DataFrame for all combinations
df = pd.DataFrame(token_estimations)
# Calculate costs for input and output for each combination
df["Input Cost (€)"] = df["Input Tokens"] * input_price
df["Output Cost (€)"] = df["Output Tokens"] * output_price

# Show the DataFrame
st.dataframe(df)

# Save DataFrame to Excel with multiple sheets
with pd.ExcelWriter("estimation_costs.xlsx") as writer:
    for characters in character_counts:
        sheet_name = f"character_counts_{characters}"
        df_filtered = df[df["Characters"] == characters]
        df_filtered.to_excel(writer, sheet_name=sheet_name, index=False)
```

This script will save the data to an Excel file (`estimation_costs.xlsx`) with each sheet named according to the `character_counts`. Each sheet will contain the corresponding data filtered based on the `character_counts`.


## Mistral