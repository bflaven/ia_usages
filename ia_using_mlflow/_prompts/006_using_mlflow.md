# 002_using_mlflow.md

## PROMPT_1
As a seasoned programmer, can you correct the script below and improve the prompt.

```python
# Define your desired data structure.
# Define the PostResponse model using Pydantic for structured output
class PostResponse(BaseModel):
    title: str = Field(description="This is the title of the post")
    summary: str = Field(description="This is the summary of the post")
    keywords: int = Field(description="This is the 5 keywords of the post")
    categorie: str = Field(description="This is the categorie of the post")

# Define the Posts model, which contains a list of PostResponse objects
class Posts(BaseModel):
    post: List[PostResponse]


parser = JsonOutputParser(pydantic_object=PostResponse)


prompt = PromptTemplate(
    template="""
system:
Tu es un expert SEO qui ne répond que en {lang}.
Etant donné le texte saisi par l'utilisateur, génère les éléments suivants:

1: Un titre concis, engageant et riche en mots clés qui représente fidèlement le contenu. Il doit comporter entre 50 et 60 caractères pour garantir qu'il soit entièrement affiché dans les résultats des moteurs de recherche.
2: Un bref résumé de 2 à 3 phrases des principaux points ou points à retenir du texte. Cela devrait également inclure un ou deux des principaux mots-clés. Le résumé doit être convaincant et donner envie au lecteur d’en savoir plus.
3: Les cinq mots-clés les plus importants et les plus pertinents extraits du texte. Il doit s'agir exlusivement de cinq mots-clés que les lecteurs potentiels pourraient utiliser pour rechercher ce type de contenu.
4: La catégorie ou le sujet principal auquel appartient le texte. Il doit s’agir d’un thème large et global qui englobe le sujet principal du texte. Cette catégorie doit être dans la langue du texte {lang} et doit appartenir aux vocabulaires IPTC NewsCodes Concept.

question:
{content}

format_instructions:
{format_instructions}

prefix:
Voici votre réponse en {lang} :
[{{ "1": "...",
   "2": "...",
   "3": [
    "...",
    "...",
    "...",
    "...",
    "..."
  ],
    "4": "..." }}]
    
""",
    input_variables=["content", "lang"],
    partial_variables={"format_instructions": parser.get_format_instructions()},

)

# And a query intended to prompt a language model to populate the data structure.
chain = prompt | model | parser
print("-------------------------------------- output\n")
output = chain.invoke({"content": content, "lang": lang})
print("\n")
```

# mistral

from typing import List
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

# Define your desired data structure.
# Define the PostResponse model using Pydantic for structured output
class PostResponse(BaseModel):
    title: str = Field(description="A concise, engaging title rich in keywords that accurately represents the content. It should be between 50 to 60 characters long to ensure it is fully displayed in search engine results.")
    summary: str = Field(description="A brief 2-3 sentence summary of the main points or takeaways from the text. This should also include one or two of the main keywords. The summary should be compelling and entice the reader to learn more.")
    keywords: List[str] = Field(description="The five most important and relevant keywords extracted from the text. These should be the keywords that potential readers might use to search for this type of content.")
    category: str = Field(description="The main theme or subject to which the text belongs. This should be a broad and general topic that encompasses the main subject of the text. The category should be in the language of the text and should belong to the IPTC NewsCodes Concept vocabulary.")

parser = PydanticOutputParser(pydantic_object=PostResponse)

prompt = PromptTemplate(
    template="""
You are an SEO expert who only responds in {lang}.
Given the user-provided text, generate the following elements:

1: A concise, engaging title rich in keywords that accurately represents the content. It should be between 50 to 60 characters long to ensure it is fully displayed in search engine results.
2: A brief 2-3 sentence summary of the main points or takeaways from the text. This should also include one or two of the main keywords. The summary should be compelling and entice the reader to learn more.
3: The five most important and relevant keywords extracted from the text. These should be the keywords that potential readers might use to search for this type of content.
4: The main theme or subject to which the text belongs. This should be a broad and general topic that encompasses the main subject of the text. The category should be in the language of the text and should belong to the IPTC NewsCodes Concept vocabulary.

Text:
{content}

{format_instructions}
""",
    input_variables=["content", "lang"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

# And a query intended to prompt a language model to populate the data structure.
model = OpenAI(temperature=0)
chain = prompt | model | parser
print("-------------------------------------- output\n")
output = chain.invoke({"content": content, "lang": lang})
print("\n")






