
# pricing_mistral_chatgpt_13.md

## prompt_1
As an advanced programmer in Streamlit, convert this code into streamlit code with a dropdown menu to select a single model inside the variable "models"

models: [{'name': 'gpt-3.5-turbo-instruct', 'description': 'Same capabilities as the standard gpt-3.5-turbo model but uses completion rather than chat completion enpoint', 'max_tokens': '4096', 'prompt_cost_per_token': '0.0015 / 1000', 'completion_cost_per_token': '0.002 / 1000'}]

```python
import streamlit as st
from llm_cost_estimation import count_tokens, models
import pandas as pd

# EXAMPLE_1
for model in models:
    print(f'Model Name: {model["name"]}')
    print(f'Completion Cost Per Token: {model["completion_cost_per_token"]}')
    print(f'Prompt Cost Per Token: {model["prompt_cost_per_token"]}')
    print(f'Maximum Tokens: {model["max_tokens"]}')
    print(f'Description: {model["description"]}\n')


# EXAMPLE_2
# Convert the list of dictionaries to a DataFrame
models_df = pd.DataFrame(models)

# Display the DataFrame
print(models_df)

```


## ChatGPT_1

To create a Streamlit app with a dropdown menu to select a single model from the `models` variable, you can follow this pattern. The dropdown will allow users to select a model, and upon selection, relevant details about the model will be displayed on the Streamlit interface. Here's how you could write this:

```bash
# Make sure you have Streamlit installed
# !pip install streamlit
```

```python
import streamlit as st
from llm_cost_estimation import models
import pandas as pd

# Title for the app
st.title("Model Information Viewer")

# Dropdown menu to select a model
model_names = [model['name'] for model in models]
selected_model_name = st.selectbox("Select a Model", model_names)

# Get the selected model details
selected_model = next(model for model in models if model['name'] == selected_model_name)

# Display information about the selected model
st.write(f"### Model Information for: {selected_model['name']}")
st.write(f"**Completion Cost Per Token**: {selected_model['completion_cost_per_token']}")
st.write(f"**Prompt Cost Per Token**: {selected_model['prompt_cost_per_token']}")
st.write(f"**Maximum Tokens**: {selected_model['max_tokens']}")
st.write(f"**Description**: {selected_model['description']}")

# Convert the list of dictionaries to a DataFrame and display it
models_df = pd.DataFrame(models)

st.write("### Overview of All Models")
st.dataframe(models_df)  # This displays the DataFrame in the Streamlit app
```

In this code snippet:
- The title and description are added to give context to the Streamlit app.
- A dropdown (`st.selectbox`) allows users to select a model.
- Information about the selected model is displayed using Streamlit's write functions.
- The full DataFrame of all models is also displayed for an overview. 

To run this code, you'd need to set up a Streamlit environment and start a Streamlit server. If you're running this in a Jupyter notebook or Google Colab, you'll need to use a different process to run Streamlit, typically by running the Streamlit code in a separate environment or setting up a Streamlit server on your local machine.


