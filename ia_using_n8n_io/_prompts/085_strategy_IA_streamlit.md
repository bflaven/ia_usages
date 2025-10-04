
# 085_strategy_IA_streamlit.md



## INPUT_4
Change the last version of the script with following changes :
1. Keep these variables into `config.py` do not remove them. Keep them as the top of the `config.py`.

```python
# Ollama configuration
OLLAMA_URL = "http://localhost:11434"  # Default Ollama URL
MODEL_NAME = "mistral:7b"              # Model name in Ollama
# MODEL_NAME = "mistral:latest"  
# MODEL_NAME = "phi3.5:3.8b"  
# MODEL_NAME = "neoali/gemma3-8k:4b"  
# MODEL_NAME = "deepseek-r1:latest"
# MODEL_NAME = "embeddinggemma:latest"
# MODEL_NAME = "gemma3:1b"
# MODEL_NAME = "gemma3n:latest"
# MODEL_NAME = "phi3:14b"
# MODEL_NAME = "life4living/ChatGPT:latest"

# Request configuration
STREAM = False  # Set to True for streaming responses
```



