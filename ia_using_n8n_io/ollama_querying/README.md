# ollama_querying

**A few scattered but interesting development elements.**

In fact, these files aren't entirely without logic. Behind them, there's this rough user story:

**rough user story**
> As the designer of an AI solution, can you write a Python script using Streamlit (UI) that will then call an execute prompt within Ollama (API), based on a defined model, e.g., mistral:7b, life4living/ChatGPT:latest, deepseek-r1:latest, etc.? The goal is to generate a title from a content suggestion and implement "retry" or "on-demand" processing to demonstrate that the result is obtained not by the evolution of the prompt or the model, but by interaction.



## improve prompt

As a digital PO, can you refine the user-storie below and print it in a ```text...``` without the readme tags such as `**`, `##`... etc.

```text
As the designer of an AI solution, can you write a Python script using Streamlit (UI) that will then call an execute prompt within Ollama (API), based on a defined model, e.g., mistral:7b, life4living/ChatGPT:latest, deepseek-r1:latest, etc.? The goal is to generate a title from a content suggestion and implement "retry" or "on-demand" processing to demonstrate that the result is obtained not by the evolution of the prompt or the model, but by interaction.
```

**improved user story**
> As a user,
I want a Python script using Streamlit to create a UI that interacts with Ollama's API.
The script should allow me to select a model (e.g., mistral:7b, life4living/ChatGPT:latest, deepseek-r1:latest)
and input a content suggestion to generate a title.
The system should support "retry" or "on-demand" processing to demonstrate that the result is derived from interaction,
not from changes in the prompt or model.



