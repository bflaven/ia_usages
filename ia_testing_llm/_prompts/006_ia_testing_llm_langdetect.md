
# 005_ia_testing_llm.md



## PROMPT_1

Act as a promptfoo expert, extend the test written in the file "assert_all.py". Here is some elemnts to understand the prompt and the result expected that is showed in "Result:".

Prompt:
```txt
Génère un objet JSON valide strictement conforme aux spécifications ci-dessous à partir du {{ content }} fourni par l'utilisateur. Aucune balise de code ou formatage supplémentaire n'est autorisé. La sortie doit être un objet JSON strict pouvant être consommé directement par une API, sans texte explicatif, sans balises ```json, ``` ou tout autre format additionnel.

Format attendu du JSON :
1. Un titre entre 50 et 60 caractères, engageant et riche en mots-clés, qui représente fidèlement le contenu.
2. Un résumé concis de 2 à 3 phrases des points principaux du texte, avec 1 ou 2 mots-clés inclus pour susciter l'intérêt du lecteur.
3. Les cinq mots-clés ou expressions les plus pertinents du texte, que les lecteurs potentiels utiliseraient pour le rechercher.
4. La catégorie générale ou le thème principal auquel appartient le contenu.

Le résultat doit être en {{ lang }} et structuré en JSON strictement comme suit :

[
  {
    \"1\": \"Titre de l'article\",
    \"2\": \"Résumé de l'article en 2-3 phrases.\",
    \"3\": [\"Mot-clé 1\", \"Mot-clé 2\", \"Mot-clé 3\", \"Mot-clé 4\", \"Mot-clé 5\"],
    \"4\": \"Catégorie ou sujet principal\"
  }
]

Ne fournis que l'objet JSON pur en {{ lang }}, sans aucune balise, texte explicatif, ou autre formatage non JSON. Le résultat doit être un JSON brut et valide, strictement conforme aux spécifications, prêt à être consommé par une API.
``` 

Config:
```yaml
description: "MLFLOW PROMPTFOO EVAL #1"

prompts: mig_prompt_1.txt
  

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
        lang: French
        content: file://articles/fr/1.txt
      assert:
        - type: contains-json
          value: file://assert/assert_all.json
        - type: python
          value: file://assert/assert_all.py
    # - vars:
    #     language: French
    #     input: file://articles/es.txt
    #   assert:
    #     - type: python
    #       value: file://assert/assert_es.py






```
Result:
```json
[ { "1": "Patrons inquiets : hausses de taxes, incertitude économique", "2": "Patrons redoutent un risque majeur en cas de victoire des partis politiques et la peur d'une période longue d'incertitude. Ils redoutent aussi des mesures restreignant l'emploi d'étrangers.", "3": ["patrons", "élection politique", "incertitude économique", "risque", "patronage"], "4": "Économie - Affaires" } ]
```





## MISTRAL_1

To extend the test written in the file `assert_all.py`, we need to ensure that the generated JSON output meets the specified criteria. The criteria include checking the length of the title, the structure of the summary, the presence of keywords, and the correct categorization. Here's how you can write the `assert_all.py` file to perform these checks:

```python
# assert_all.py

import json

def get_assert(output, context):
    print("Prompt:", context["prompt"])
    print("Vars", context["vars"]["lang"])
    print("Vars", context["vars"]["content"])

    try:
        # Parse the output as JSON
        output_json = json.loads(output)

        # Check if the output is a list with one dictionary
        if not isinstance(output_json, list) or len(output_json) != 1 or not isinstance(output_json[0], dict):
            return {
                "pass": False,
                "score": 0.0,
                "reason": "Output is not a list with one dictionary."
            }

        item = output_json[0]

        # Check the title length
        title = item.get("1", "")
        if not (50 <= len(title) <= 60):
            return {
                "pass": False,
                "score": 0.0,
                "reason": "Title length is not between 50 and 60 characters."
            }

        # Check the summary structure
        summary = item.get("2", "")
        if not (2 <= summary.count('.') <= 3):
            return {
                "pass": False,
                "score": 0.0,
                "reason": "Summary does not contain 2 to 3 sentences."
            }

        # Check the keywords
        keywords = item.get("3", [])
        if not (isinstance(keywords, list) and len(keywords) == 5):
            return {
                "pass": False,
                "score": 0.0,
                "reason": "Keywords are not a list of 5 items."
            }

        # Check the category
        category = item.get("4", "")
        if not category:
            return {
                "pass": False,
                "score": 0.0,
                "reason": "Category is missing."
            }

        # All checks passed
        return {
            "pass": True,
            "score": 1.0,
            "reason": "All checks passed."
        }

    except json.JSONDecodeError:
        return {
            "pass": False,
            "score": 0.0,
            "reason": "Output is not a valid JSON."
        }

```

In this script:

1. **JSON Parsing**: The output is parsed as JSON.
2. **Structure Check**: The script checks if the output is a list with one dictionary.
3. **Title Length**: The script verifies that the title length is between 50 and 60 characters.
4. **Summary Structure**: The script checks that the summary contains 2 to 3 sentences.
5. **Keywords**: The script ensures that the keywords are a list of exactly 5 items.
6. **Category**: The script verifies that the category is present.

If any of these checks fail, the script returns a failure message with a score of 0.0. If all checks pass, it returns a success message with a score of 1.0.

This script can be further extended to include more detailed checks or additional criteria as needed.
