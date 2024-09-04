# 002_using_mlflow.md

## PROMPT_1
As an advanced programmer in Python and in Ollama, make this code wok and give an example

```python
from pydantic import BaseModel, Field
from typing import List

from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser
from pydantic.v1 import ValidationError

from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain.output_parsers import PydanticOutputParser

from langchain.prompts import PromptTemplate

class CityResponse(BaseModel):
    city_name: str = Field(description="This is the Name of the city")
    country: str = Field(description="This is the country of the city")
    population_number: int = Field(description="This is the number of inhabitants")
    local_currency: str = Field(description="This is the local currency of the city")

class Cities(BaseModel):
    city: List[CityResponse]

llm = Ollama(model="mistral:latest")

pydantic_parser = PydanticOutputParser(pydantic_object=Cities)

query = "What are the top three big cities in Europe by population?"
prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": pydantic_parser.get_format_instructions()},
)

# Construct a Langchain Chain to connect the prompt template with the LLM and Pydantic parser
chain = prompt | llm | StrOutputParser
```



