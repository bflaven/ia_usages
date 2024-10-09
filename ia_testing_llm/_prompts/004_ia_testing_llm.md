
# 004_ia_testing_llm.md



## PROMPT_1

Act as a promptfoo expert, extend the test written in the file "assert_es.py" 

```yaml
# Learn more about building a configuration: https://promptfoo.dev/docs/configuration/guide
description: "My eval"

prompts:
  # - 'Convert this text to {{language}}: {{input}}'
  - 'Translate to {{language}}: {{input}}'
  

providers:
  - id: ollama:mistral:latest
    config:
      temperature: 0.8
#  - id: openrouter:mistralai/mixtral-8x7b-instruct
#    config:
#      temperature: 0.5
#  - id: openrouter:meta-llama/llama-3.1-8b-instruct
#    config:
#      temperature: 0.5

scenarios:
  - config:
      - vars:
          value_1: hello
          # value_2: bonjour
          
    tests:
    - vars:
        language: French
        input: file://articles/en_2.txt
      assert:
        - type: python
          value: file://assert/assert_es.py
    # - vars:
    #     language: French
    #     input: file://articles/es.txt
    #   assert:
    #     - type: python
    #       value: file://assert/assert_es.py

```

```python
# assert_es.py

def get_assert(output, context):
    print("Prompt:", context["prompt"])
    print("Vars", context["vars"]["language"])    
    print("Vars", context["vars"]["input"])
    
    result = {
            "pass": "comment" in output.lower(),
            "score": 0.5,
            "reason": "Contains comment",
        }

    

    return result


```





## MISTRAL_1

To extend the test written in the file `assert_es.py`, we can add more assertions and improve the logic to handle different scenarios. Here's an updated version of the `assert_es.py` file with additional checks and a more detailed evaluation:

```python
# assert_es.py

def get_assert(output, context):
    print("Prompt:", context["prompt"])
    print("Vars", context["vars"]["language"])
    print("Vars", context["vars"]["input"])

    # Check if the output contains specific keywords related to the language
    language = context["vars"]["language"].lower()
    if language == "french":
        keywords = ["bonjour", "merci", "au revoir"]
    elif language == "spanish":
        keywords = ["hola", "gracias", "adiós"]
    elif language == "german":
        keywords = ["hallo", "danke", "auf wiedersehen"]
    else:
        keywords = []

    # Check if the output contains any of the keywords
    contains_keyword = any(keyword in output.lower() for keyword in keywords)

    # Additional checks can be added here, such as checking the length of the output
    min_length = 50  # Minimum expected length of the output
    sufficient_length = len(output) >= min_length

    # Calculate the score based on the checks
    score = 0.5 if contains_keyword else 0.0
    score += 0.5 if sufficient_length else 0.0

    result = {
        "pass": contains_keyword and sufficient_length,
        "score": score,
        "reason": f"Contains keyword: {contains_keyword}, Sufficient length: {sufficient_length}",
    }

    return result
```

In this updated version, the `get_assert` function now checks if the output contains specific keywords related to the target language. It also checks if the output has a sufficient length. The score is calculated based on these checks, and the result includes a more detailed reason for the evaluation.

You can further extend this function by adding more checks and improving the logic to handle different scenarios and requirements.
