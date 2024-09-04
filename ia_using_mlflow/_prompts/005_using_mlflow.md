# 002_using_mlflow.md

## PROMPT_1
As a seasoned programmer, can you correct the script below and make it work.

```python
# Define the query and the prompt template
prompt = PromptTemplate(
    template="""
system = "
Tu es un expert SEO qui ne répond que en {lang}.
Etant donné le texte par l'utilisateur, génère les éléments suivants:
1. Un titre concis, engageant et riche en mots clés qui représente fidèlement le contenu. Il doit comporter entre 50 et 60 caractères pour garantir qu'il soit entièrement affiché dans les résultats des moteurs de recherche.
2. Un bref résumé de 2 à 3 phrases des principaux points ou points à retenir du texte. Cela devrait également inclure un ou deux des principaux mots-clés. Le résumé doit être convaincant et donner envie au lecteur d’en savoir plus.
3. Les cinq mots-clés ou expressions les plus importants et les plus pertinents extraits du texte. Il doit s'agir de mots ou d'expressions que les lecteurs potentiels pourraient utiliser pour rechercher ce type de contenu.
4. La catégorie ou le sujet principal auquel appartient le texte. Il doit s’agir d’un thème large et global qui englobe le sujet principal du texte.
"
question = "
{content}
"
prefix = "
Voici votre réponse en {lang} :
[{ "1": "...",
   "2": "...",
   "3": [
    "...",
    "...",
    "...",
    "...",
    "..."
  ],
    "4": "..." }]
"
    """,
    input_variables=["query"],
)

# And a query intended to prompt a language model to populate the data structure.
chain = prompt | model
print("-------------------------------------- output\n")
output = chain.invoke({"content": content, "lang": lang})
print("\n")
```

# mistral

from langchain import PromptTemplate, LLMChain
from langchain.llms import OpenAI

# Define the query and the prompt template
prompt = PromptTemplate(
    template="""
system:
Tu es un expert SEO qui ne répond que en {lang}.
Etant donné le texte par l'utilisateur, génère les éléments suivants:
1. Un titre concis, engageant et riche en mots clés qui représente fidèlement le contenu. Il doit comporter entre 50 et 60 caractères pour garantir qu'il soit entièrement affiché dans les résultats des moteurs de recherche.
2. Un bref résumé de 2 à 3 phrases des principaux points ou points à retenir du texte. Cela devrait également inclure un ou deux des principaux mots-clés. Le résumé doit être convaincant et donner envie au lecteur d’en savoir plus.
3. Les cinq mots-clés ou expressions les plus importants et les plus pertinents extraits du texte. Il doit s'agir de mots ou d'expressions que les lecteurs potentiels pourraient utiliser pour rechercher ce type de contenu.
4. La catégorie ou le sujet principal auquel appartient le texte. Il doit s’agir d’un thème large et global qui englobe le sujet principal du texte.

question:
{content}

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
)

# Define the language model
model = OpenAI(temperature=0.7)

# Create a language model chain
chain = LLMChain(llm=model, prompt=prompt)

# Define the content and language
content = "Your input text here"
lang = "French"

# Generate the SEO-friendly content
output = chain.run({"content": content, "lang": lang})
print("-------------------------------------- output\n")
print(output)
print("\n")





