
# 001_ia_testing_llm.md


## PROMPT_1
Act as a Python expert, fix the script below and avoid the errors : ```* 'allow_population_by_field_name' has been renamed to 'populate_by_name' * 'smart_union' has been removed warnings.warn(message, UserWarning)```




```python
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List
import instructor


class Character(BaseModel):
    name: str
    age: int
    fact: List[str] = Field(..., description="A list of facts about the character")


# enables `response_model` in create call
client = instructor.from_openai(
    OpenAI(
        # http://127.0.0.1:11434
        base_url="http://localhost:11434/v1",
        api_key="ollama",  # required, but unused
    ),
    mode=instructor.Mode.JSON,
    # Update configuration keys
    populate_by_name=True,  # Replace 'allow_population_by_field_name' with 'populate_by_name'

)

resp = client.chat.completions.create(
    # model="llama3",
    model="mistral:latest",
    messages=[
        {
            "role": "user",
            "content": "Tell me about the Harry Potter",
        }
    ],
    response_model=Character,
)
print(resp.model_dump_json(indent=2))
```







## CHATGPT_1

