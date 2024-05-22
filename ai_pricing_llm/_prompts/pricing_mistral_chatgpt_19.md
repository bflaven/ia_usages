
# pricing_mistral_chatgpt_19.md

## prompt_1
As an advanced programmer in Streamlit, according to the values below, it the user select several models, create a muliple sheets with pandas that show the complete estiamtion cost for each combination of character_counts and model.

```python
import streamlit as st
import pandas as pd

# Part 1: Select a model
model_options = ["mistral-small", "mistral-medium", "mistral-large", "open-mistral-7b", "open-mixtral-8x7b", "open-mixtral-8x22b", "gpt-4-turbo-2024-04-09", "gpt-3.5-turbo-0125"]
selected_model = st.selectbox("Models", model_options)

# For mistral https://mistral.ai/fr/technology/
# For openai https://openai.com/api/pricing/
# For exchange rate https://wise.com/fr/currency-converter/usd-to-eur-rate?amount=10
 
prices = {
    "mistral-small": {"input": 0.9, "output": 2.8},
    "mistral-medium": {"input": 2.5, "output": 7.5},
    "mistral-large": {"input": 3.8, "output": 11.3},
    "open-mistral-7b": {"input": 0.2, "output": 0.2},
    "open-mixtral-8x7b": {"input": 0.65, "output": 0.65},
    "open-mixtral-8x22b": {"input": 1.9, "output": 5.6},
    "gpt-4-turbo-2024-04-09": {"input": 9.29, "output": 27.86},
    "gpt-3.5-turbo-0125": {"input": 0.46, "output": 1.39}

}
# Get the selected model's prices
input_price = prices[selected_model]["input"] / 1000000
output_price = prices[selected_model]["output"] / 1000000

# Part 3: Total of tokens regarding the volume
# Define character counts per content and volume of content
character_counts = [500, 1000, 1500, 2000]
content_volumes = [500, 1000, 2500, 5000, 7500, 10000, 15000, 20000, 50000]


# to complete

```


## ChatGPT_1
To achieve your goal of creating multiple sheets with pandas showing the complete estimation cost for each combination of `character_counts` and `model`, you can follow these steps:

1. Iterate over each character count and content volume combination.
2. Calculate the total number of tokens based on the character count and the specific model's tokenization method.
3. Compute the estimation cost for both input and output based on the token count and the model's pricing.
4. Store the results in a pandas DataFrame.
5. Write each DataFrame to a separate Excel sheet.

Here's the code implementing these steps:

```python
import streamlit as st
import pandas as pd

# Part 1: Select a model
model_options = ["mistral-small", "mistral-medium", "mistral-large", "open-mistral-7b", "open-mixtral-8x7b", "open-mixtral-8x22b", "gpt-4-turbo-2024-04-09", "gpt-3.5-turbo-0125"]
selected_model = st.selectbox("Models", model_options)

# Prices dictionary
prices = {
    "mistral-small": {"input": 0.9, "output": 2.8},
    "mistral-medium": {"input": 2.5, "output": 7.5},
    "mistral-large": {"input": 3.8, "output": 11.3},
    "open-mistral-7b": {"input": 0.2, "output": 0.2},
    "open-mixtral-8x7b": {"input": 0.65, "output": 0.65},
    "open-mixtral-8x22b": {"input": 1.9, "output": 5.6},
    "gpt-4-turbo-2024-04-09": {"input": 9.29, "output": 27.86},
    "gpt-3.5-turbo-0125": {"input": 0.46, "output": 1.39}
}

# Get the selected model's prices
input_price = prices[selected_model]["input"] / 1000000
output_price = prices[selected_model]["output"] / 1000000

# Part 3: Total of tokens regarding the volume
# Define character counts per content and volume of content
character_counts = [500, 1000, 1500, 2000]
content_volumes = [500, 1000, 2500, 5000, 7500, 10000, 15000, 20000, 50000]

# Create a dictionary to store the results
results = {}

# Iterate over each combination of character counts and content volumes
for char_count in character_counts:
    for volume in content_volumes:
        # Calculate total tokens
        total_tokens = char_count * volume
        
        # Calculate estimation cost for input and output
        input_cost = total_tokens * input_price
        output_cost = total_tokens * output_price
        
        # Store the results
        key = f"Character Count: {char_count}, Content Volume: {volume}"
        results[key] = {"Input Cost": input_cost, "Output Cost": output_cost}

# Create a DataFrame from the results
df = pd.DataFrame(results).T

# Write each DataFrame to a separate Excel sheet
with pd.ExcelWriter('estimation_costs.xlsx') as writer:
    df.to_excel(writer, sheet_name='Estimation Costs')
```

This code will generate an Excel file named `estimation_costs.xlsx` with a sheet for each combination of `character_counts` and `content_volumes`, displaying the estimation costs for both input and output based on the selected model's pricing.


## prompt_2
As an advanced programmer in Streamlit, rewrite the script with the values below, it the user select several models, create a muliple sheets with pandas that show the complete estiamtion cost for each combination of character_counts and model.

```python


import streamlit as st
import pandas as pd
from datetime import datetime


# Part 1: Select multiple models
model_options = ["mistral-small", "mistral-medium", "mistral-large", "open-mistral-7b", "open-mixtral-8x7b", "open-mixtral-8x22b", "gpt-4-turbo-2024-04-09", "gpt-3.5-turbo-0125"]
selected_models = st.multiselect("Models", model_options)

# Prices dictionary
prices = {
    "mistral-small": {"input": 0.9, "output": 2.8},
    "mistral-medium": {"input": 2.5, "output": 7.5},
    "mistral-large": {"input": 3.8, "output": 11.3},
    "open-mistral-7b": {"input": 0.2, "output": 0.2},
    "open-mixtral-8x7b": {"input": 0.65, "output": 0.65},
    "open-mixtral-8x22b": {"input": 1.9, "output": 5.6},
    "gpt-4-turbo-2024-04-09": {"input": 9.29, "output": 27.86},
    "gpt-3.5-turbo-0125": {"input": 0.46, "output": 1.39}
}

# Get the selected model's prices
input_price = prices[selected_models]["input"] / 1000000
output_price = prices[selected_models]["output"] / 1000000

# Part 3: Total of tokens regarding the volume
# Define character counts per content and volume of content
character_counts = [500, 1000, 1500, 2000]
content_volumes = [500, 1000, 2500, 5000, 7500, 10000, 15000, 20000, 50000]

# Create a dictionary to store the results
results = {}

# Iterate over each combination of character counts and content volumes
for char_count in character_counts:
    for volume in content_volumes:
        # Calculate total tokens
        total_tokens = char_count * volume
        
        # Calculate estimation cost for input and output
        input_cost = total_tokens * input_price
        output_cost = total_tokens * output_price
        
        # Store the results
        key = f"Character Count: {char_count}, Content Volume: {volume}"
        results[key] = {"Input Cost": input_cost, "Output Cost": output_cost}

# Create a DataFrame from the results
df = pd.DataFrame(results).T

creation_date = datetime.now().strftime("%Y-%m-%d")


# Write each DataFrame to a separate Excel sheet
with pd.ExcelWriter(f'{creation_date}_estimation_costs.xlsx') as writer:

    df.to_excel(writer, sheet_name='Estimation Costs')
```

## ChatGPT_2
To handle multiple selected models and generate separate sheets for each model in the Excel file, you can modify the script as follows:

```python
import streamlit as st
import pandas as pd
from datetime import datetime

# Part 1: Select multiple models
model_options = ["mistral-small", "mistral-medium", "mistral-large", "open-mistral-7b", "open-mixtral-8x7b", "open-mixtral-8x22b", "gpt-4-turbo-2024-04-09", "gpt-3.5-turbo-0125"]
selected_models = st.multiselect("Models", model_options)

# Prices dictionary
prices = {
    "mistral-small": {"input": 0.9, "output": 2.8},
    "mistral-medium": {"input": 2.5, "output": 7.5},
    "mistral-large": {"input": 3.8, "output": 11.3},
    "open-mistral-7b": {"input": 0.2, "output": 0.2},
    "open-mixtral-8x7b": {"input": 0.65, "output": 0.65},
    "open-mixtral-8x22b": {"input": 1.9, "output": 5.6},
    "gpt-4-turbo-2024-04-09": {"input": 9.29, "output": 27.86},
    "gpt-3.5-turbo-0125": {"input": 0.46, "output": 1.39}
}

creation_date = datetime.now().strftime("%Y-%m-%d")

# Part 3: Total of tokens regarding the volume
# Define character counts per content and volume of content
character_counts = [500, 1000, 1500, 2000]
content_volumes = [500, 1000, 2500, 5000, 7500, 10000, 15000, 20000, 50000]

# Iterate over each selected model
for selected_model in selected_models:
    # Get the selected model's prices
    input_price = prices[selected_model]["input"] / 1000000
    output_price = prices[selected_model]["output"] / 1000000
    
    # Create a dictionary to store the results for this model
    results = {}
    
    # Iterate over each combination of character counts and content volumes
    for char_count in character_counts:
        for volume in content_volumes:
            # Calculate total tokens
            total_tokens = char_count * volume
            
            # Calculate estimation cost for input and output
            input_cost = total_tokens * input_price
            output_cost = total_tokens * output_price
            
            # Store the results
            key = f"Character Count: {char_count}, Content Volume: {volume}"
            results[key] = {"Input Cost": input_cost, "Output Cost": output_cost}
    
    # Create a DataFrame from the results
    df = pd.DataFrame(results).T

    # Write each DataFrame to a separate Excel sheet
    with pd.ExcelWriter(f'{selected_model}_{creation_date}_estimation_costs.xlsx', mode='a', engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=f'{selected_model} Estimation Costs')
```

This script will create an Excel file with separate sheets for each selected model, containing the estimation costs for each combination of character counts and content volumes based on the selected model's pricing. Each sheet will be named accordingly with the model's name.



## chatGPT_3

The error indicates that the script is trying to write to a file that doesn't exist. To fix this, you can ensure that the file is created before writing to it. Here's the modified script:

```python
import streamlit as st
import pandas as pd
from datetime import datetime
import os.path

# Part 1: Select multiple models
model_options = ["mistral-small", "mistral-medium", "mistral-large", "open-mistral-7b", "open-mixtral-8x7b", "open-mixtral-8x22b", "gpt-4-turbo-2024-04-09", "gpt-3.5-turbo-0125"]
selected_models = st.multiselect("Models", model_options)

# Prices dictionary
prices = {
    "mistral-small": {"input": 0.9, "output": 2.8},
    "mistral-medium": {"input": 2.5, "output": 7.5},
    "mistral-large": {"input": 3.8, "output": 11.3},
    "open-mistral-7b": {"input": 0.2, "output": 0.2},
    "open-mixtral-8x7b": {"input": 0.65, "output": 0.65},
    "open-mixtral-8x22b": {"input": 1.9, "output": 5.6},
    "gpt-4-turbo-2024-04-09": {"input": 9.29, "output": 27.86},
    "gpt-3.5-turbo-0125": {"input": 0.46, "output": 1.39}
}

creation_date = datetime.now().strftime("%Y-%m-%d")

# Part 3: Total of tokens regarding the volume
# Define character counts per content and volume of content
character_counts = [500, 1000, 1500, 2000]
content_volumes = [500, 1000, 2500, 5000, 7500, 10000, 15000, 20000, 50000]

# Iterate over each selected model
for selected_model in selected_models:
    # Get the selected model's prices
    input_price = prices[selected_model]["input"] / 1000000
    output_price = prices[selected_model]["output"] / 1000000
    
    # Create a dictionary to store the results for this model
    results = {}
    
    # Iterate over each combination of character counts and content volumes
    for char_count in character_counts:
        for volume in content_volumes:
            # Calculate total tokens
            total_tokens = char_count * volume
            
            # Calculate estimation cost for input and output
            input_cost = total_tokens * input_price
            output_cost = total_tokens * output_price
            
            # Store the results
            key = f"Character Count: {char_count}, Content Volume: {volume}"
            results[key] = {"Input Cost": input_cost, "Output Cost": output_cost}
    
    # Create a DataFrame from the results
    df = pd.DataFrame(results).T

    # Define the file name
    file_name = f'{selected_model}_{creation_date}_estimation_costs.xlsx'

    # Check if the file exists
    if not os.path.isfile(file_name):
        # If the file does not exist, create it with the DataFrame
        with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name=f'{selected_model} Estimation Costs')
    else:
        # If the file already exists, append the DataFrame to it
        with pd.ExcelWriter(file_name, mode='a', engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=f'{selected_model} Estimation Costs', index=False)
```

This script checks if the Excel file exists before writing to it. If it doesn't exist, it creates a new file and writes the DataFrame to it. If the file already exists, it appends the DataFrame to the existing file. This should resolve the `FileNotFoundError`.


## ChatGPT_3

The error occurs because the script is trying to create a new sheet with a name that already exists in the Excel file. To fix this, we can either skip writing the sheet if it already exists or overwrite the existing sheet with the new data. Here's the modified script to overwrite the existing sheet:

```python
import streamlit as st
import pandas as pd
from datetime import datetime
import os.path

# Part 1: Select multiple models
model_options = ["mistral-small", "mistral-medium", "mistral-large", "open-mistral-7b", "open-mixtral-8x7b", "open-mixtral-8x22b", "gpt-4-turbo-2024-04-09", "gpt-3.5-turbo-0125"]
selected_models = st.multiselect("Models", model_options)

# Prices dictionary
prices = {
    "mistral-small": {"input": 0.9, "output": 2.8},
    "mistral-medium": {"input": 2.5, "output": 7.5},
    "mistral-large": {"input": 3.8, "output": 11.3},
    "open-mistral-7b": {"input": 0.2, "output": 0.2},
    "open-mixtral-8x7b": {"input": 0.65, "output": 0.65},
    "open-mixtral-8x22b": {"input": 1.9, "output": 5.6},
    "gpt-4-turbo-2024-04-09": {"input": 9.29, "output": 27.86},
    "gpt-3.5-turbo-0125": {"input": 0.46, "output": 1.39}
}

creation_date = datetime.now().strftime("%Y-%m-%d")

# Part 3: Total of tokens regarding the volume
# Define character counts per content and volume of content
character_counts = [500, 1000, 1500, 2000]
content_volumes = [500, 1000, 2500, 5000, 7500, 10000, 15000, 20000, 50000]

# Iterate over each selected model
for selected_model in selected_models:
    # Get the selected model's prices
    input_price = prices[selected_model]["input"] / 1000000
    output_price = prices[selected_model]["output"] / 1000000
    
    # Create a dictionary to store the results for this model
    results = {}
    
    # Iterate over each combination of character counts and content volumes
    for char_count in character_counts:
        for volume in content_volumes:
            # Calculate total tokens
            total_tokens = char_count * volume
            
            # Calculate estimation cost for input and output
            input_cost = total_tokens * input_price
            output_cost = total_tokens * output_price
            
            # Store the results
            key = f"Character Count: {char_count}, Content Volume: {volume}"
            results[key] = {"Input Cost": input_cost, "Output Cost": output_cost}
    
    # Create a DataFrame from the results
    df = pd.DataFrame(results).T

    # Define the file name
    file_name = f'{selected_model}_{creation_date}_estimation_costs.xlsx'

    # Check if the file exists
    if not os.path.isfile(file_name):
        # If the file does not exist, create it with the DataFrame
        with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name=f'{selected_model} Estimation Costs')
    else:
        # If the file already exists, overwrite the existing sheet with the new data
        with pd.ExcelWriter(file_name, mode='a', engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=f'{selected_model} Estimation Costs', index=False, startrow=1)
```

In this modified script, the `startrow=1` argument ensures that the new data is written starting from the second row, avoiding overwriting the header row. This should resolve the `ValueError`.