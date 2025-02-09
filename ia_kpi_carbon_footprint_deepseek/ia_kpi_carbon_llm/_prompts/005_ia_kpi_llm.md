
# 004_ia_kpi_llm.md


## PROMPT_1
As a python expert, make this script works and rewrite the all script so I can cut and paste


```python
modelfile='''
FROM deepseek-r1:latest
SYSTEM You are a poet but you like to keep it simple
PARAMETER temperature 5
'''



ollama.create(model='deepseek-r1:latest', modelfile=modelfile)
tracker = EmissionsTracker(save_to_api=True, tracking_mode="process")
model = "deepseek-r1:latest" # You need to pull the model from the CLI
n_poems = 10
# Start tracking
tracker.start()
poems = []
for i in range(n_poems):
    response = ollama.chat(model=model, messages=[{'role': 'user', 'content': 'Write a poem for me about open source software'}])
    poems.append(response['message']['content'])

emmissions = tracker.stop()
```

## PERPLEXITY_1








