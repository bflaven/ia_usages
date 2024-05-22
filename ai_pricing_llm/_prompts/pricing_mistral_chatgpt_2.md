
# pricing_mistral_chatgpt_2.md


## prompt

As an advanced programmer in Streamlit, create an streamlit file that allows you to make a LOW estimation and a HIGH estimation for the cost of using the following models: "mistral-small, mistral-medium, mistral-large, open-mistral-7b, open-mixtral-8x7b, open-mixtral-8x22b". Here is the precises variables, values and instructions.


1. The models must be available in dropdown named "model_name".

2. The following variables must be configurable via a drop-down menu:
nb_words_item = Number of words per article
multiplier_low = Coef LOW number of tokens per article
multiplier_high = Coef HIGH number of tokens per article
price_input = Price of the input (input)
price_output = Price of output
volume_items = Volume or Number of contents


3. The values are as follows:
Number of words per content = 500, 1000, 1500, 2000
BAS coef number of tokens per item = 1.33
Coef HIGH number of tokens per item = 1.5
Volume or Number of contents = 1,000, 50,000, 100,000...


4. Price per model


For model "mistral-small"
Input price = €1.85 per 1 Million tokens
Output price = €5.55 per 1 Million tokens

For model "mistral-medium
Input price = 2.5€ per 1 Million tokens
Output price = 7.5€ per 1 Million tokens


For model "mistral-large"
Input price = 7.3€ per 1 Million tokens
Output price = 22€ per 1 Million tokens


For model "open-mistral-7b"
Input price = 0.2€ per 1 Million tokens
Output price = 0.2€ per 1 Million tokens

For model "open-mixtral-8x7b" 
Input price = 0.65€ per 1 Million tokens
Output price = 0.65€ per 1 Million tokens

For model "open-mixtral-8x22b"
Input price = 1.9€ per 1 Million tokens
Output price = 5.6€ per 1 Million tokens






## ChatGPT
Here's a Streamlit application that allows you to estimate the low and high cost of using the specified models. It offers a dropdown for selecting the model, along with configurable variables for estimating the cost.

```python
import streamlit as st

# Model configurations with corresponding input/output prices
models = {
    "mistral-small": {"input_price": 1.85, "output_price": 5.55},
    "mistral-medium": {"input_price": 2.5, "output_price": 7.5},
    "mistral-large": {"input_price": 7.3, "output_price": 22},
    "open-mistral-7b": {"input_price": 0.2, "output_price": 0.2},
    "open-mixtral-8x7b": {"input_price": 0.65, "output_price": 0.65},
    "open-mixtral-8x22b": {"input_price": 1.9, "output_price": 5.6},
}

# Define dropdown options
words_per_article_options = [500, 1000, 1500, 2000]
volume_items_options = [1000, 50000, 100000]
multiplier_low = 1.33
multiplier_high = 1.5

# Streamlit Interface
st.title("Cost Estimation for Language Models")

# Model selection dropdown
model_name = st.selectbox("Select Model", list(models.keys()))

# Variable configuration
nb_words_item = st.selectbox("Number of Words per Content", words_per_article_options)
volume_items = st.selectbox("Volume (Number of Contents)", volume_items_options)

# Get model pricing
model_prices = models[model_name]
price_input = model_prices["input_price"]
price_output = model_prices["output_price"]

# Calculate token counts and costs
tokens_low = nb_words_item * multiplier_low
tokens_high = nb_words_item * multiplier_high

# Calculate costs (input and output)
cost_low = (tokens_low * price_input * volume_items) / 1_000_000
cost_high = (tokens_high * price_output * volume_items) / 1_000_000

# Display results
st.write("**Model Name**:", model_name)
st.write("**Number of Tokens (Low)**:", round(tokens_low, 2))
st.write("**Number of Tokens (High)**:", round(tokens_high, 2))
st.write("**Cost Estimation (Low)**: €", round(cost_low, 2))
st.write("**Cost Estimation (High)**: €", round(cost_high, 2))
```

### Instructions to Run
1. Save the above code into a file, e.g., `cost_estimation.py`.
2. In the terminal, navigate to the directory containing this file.
3. Run Streamlit using the command:
   ```bash
   streamlit run mistral_cost_estimation_1.py
   ```
4. A new browser window will open showing the Streamlit app. You can choose the model, number of words, and volume to calculate the cost estimations. The results will be displayed with both low and high estimates based on the selected configurations.

The above script implements the dropdown for model selection and the additional configurable variables, taking into account the specified prices for each model. It calculates and displays the low and high estimations accordingly.

## MISTRAL

Sure, here's a Streamlit application that fulfills your requirements:

```python
import streamlit as st

# Title
st.title('Cost Estimation App')

# Model Name
model_name = st.selectbox('Model Name', ['mistral-small', 'mistral-medium', 'mistral-large', 'open-mistral-7b', 'open-mixtral-8x7b', 'open-mixtral-8x22b'])

# Number of words per item
nb_words_item = st.selectbox('Number of words per item', [500, 1000, 1500, 2000])

# Coef LOW number of tokens per item
multiplier_low = st.selectbox('Coef LOW number of tokens per item', [1.33])

# Coef HIGH number of tokens per item
multiplier_high = st.selectbox('Coef HIGH number of tokens per item', [1.5])

# Volume or Number of contents
volume_items = st.selectbox('Volume or Number of contents', [1000, 50000, 100000])

# Price per model
model_prices = {
    'mistral-small': {'input': 1.85, 'output': 5.55},
    'mistral-medium': {'input': 2.5, 'output': 7.5},
    'mistral-large': {'input': 7.3, 'output': 22},
    'open-mistral-7b': {'input': 0.2, 'output': 0.2},
    'open-mixtral-8x7b': {'input': 0.65, 'output': 0.65},
    'open-mixtral-8x22b': {'input': 1.9, 'output': 5.6}
}

price_input = model_prices[model_name]['input']
price_output = model_prices[model_name]['output']

# Calculate LOW estimation
low_estimation = (nb_words_item * multiplier_low * price_input / 1000000) * volume_items

# Calculate HIGH estimation
high_estimation = (nb_words_item * multiplier_high * price_output / 1000000) * volume_items

# Display the estimations
st.write('LOW Estimation:', low_estimation)
st.write('HIGH Estimation:', high_estimation)
```

This application will display dropdown menus for the model name, number of words per item, coef low number of tokens per item, coef high number of tokens per item, and volume or number of contents. It will then calculate the low and high estimations based on the selected values and the prices associated with the selected model, and display these estimations.


