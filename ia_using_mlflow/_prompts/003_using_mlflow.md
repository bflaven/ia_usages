# 002_using_mlflow.md

## PROMPT_1
As an advanced programmer in Python and in Ollama, write a script that will convert this code for ollama completion with the function `llm = Ollama(model="mistral:latest")`


```python
import openai

def get_completion(prompt: str, model: str = "gpt-35-turbo") -> str:
    """
    Query your LLM model with your prompt.
    Parameters:
    prompt (str): The text prompt you want the LLM to respond to.
    model (str, optional): The model to be used for generating the response. Default is "gpt-3.5-turbo".
    Returns:
    str: The generated text completion from the specified model.
    """
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model= model,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message["content"]
```



