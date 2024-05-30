# w4_prompts_seo_dev.md

## prompt_1
As an advanced programmer in Python, write a script with if else  for this code depending on the variable "model_selected"



```python

    # for model_selected = "gpt-3.5-turbo"
    input_price = response.usage.prompt_tokens * (0.46 / 1e6)
    output_price = response.usage.completion_tokens * (1.38 / 1e6)


    # for model_selected = "gpt-4-turbo"
    input_price = response.usage.prompt_tokens * (9.18 / 1e6)
    output_price = response.usage.completion_tokens * (27.55 / 1e6)
    

```



## Mistral

Sure, I can help you with that. Here's a Python script that uses an if-else statement to calculate `input_price` and `output_price` based on the `model_selected` variable:

```python
# Assuming response and model_selected are defined and have valid values

if model_selected == "gpt-3.5-turbo":
    input_price = response.usage.prompt_tokens * (0.46 / 1e6)
    output_price = response.usage.completion_tokens * (1.38 / 1e6)
else:
    if model_selected == "gpt-4-turbo":
        input_price = response.usage.prompt_tokens * (9.18 / 1e6)
        output_price = response.usage.completion_tokens * (27.55 / 1e6)
    else:
        print("Invalid model selected. Please choose between 'gpt-3.5-turbo' and 'gpt-4-turbo'.")
```

This script first checks if `model_selected` is equal to "gpt-3.5-turbo". If it is, it calculates `input_price` and `output_price` using the provided formulas. If it's not, it checks if `model_selected` is equal to "gpt-4-turbo". If it is, it calculates `input_price` and `output_price` using the different formulas. If `model_selected` is neither "gpt-3.5-turbo" nor "gpt-4-turbo", it prints an error message.