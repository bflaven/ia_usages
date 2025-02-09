
# 002_ia_infox.md

## PROMPT_1
Donne-moi des outils en ligne ou des packages python open-source qui permmettent de faire du fact-checking.

## CHATGPT_1
Voici quelques outils en ligne et bibliothèques Python open-source qui permettent d'automatiser ou d'assister le **fact-checking** :

---

## **Outils en ligne de fact-checking :**

1. **Google Fact Check Explorer**  
   - Permet de rechercher des informations vérifiées par des organismes de fact-checking à partir d'une base mondiale.
   - Accès : [https://toolbox.google.com/factcheck/explorer](https://toolbox.google.com/factcheck/explorer)

2. **Snopes**  
   - Une des principales plateformes de vérification des faits pour démystifier les fausses informations et les rumeurs.  
   - Accès : [https://www.snopes.com](https://www.snopes.com)

3. **PolitiFact**  
   - Conçu pour évaluer la véracité des affirmations politiques, avec un système de classement (True, False, Pants on Fire, etc.).
   - Accès : [https://www.politifact.com](https://www.politifact.com)

4. **AFP Fact Check**  
   - Service global de fact-checking proposé par l'Agence France-Presse.  
   - Accès : [https://factcheck.afp.com](https://factcheck.afp.com)

5. **ClaimReview API**  
   - Une API qui structure des données issues des vérifications publiées par des sites partenaires de Google.  
   - Accès : [https://developers.google.com/search/docs/appearance/structured-data/factcheck](https://developers.google.com/search/docs/appearance/structured-data/factcheck)

---

## **Packages Python pour le fact-checking :**

1. **`newsplease`**  
   - Description : Une bibliothèque permettant d'extraire et d'analyser des articles de presse à partir d'une URL.  
   - Use-case : Comparer des articles pour détecter les différences ou extraire des faits clés.  
   - Installation : `pip install news-please`  
   - [GitHub](https://github.com/fhamborg/news-please)

2. **`spacy` + `spacy-llm`**  
   - Description : SpaCy permet d'analyser des textes pour extraire des entités, des faits et des informations clés. Avec `spacy-llm`, il est possible d'intégrer des LLM (comme GPT) pour générer des vérifications plus complexes.  
   - Use-case : Extraire des faits d’un article et comparer à des bases de vérité.  
   - Installation : `pip install spacy spacy-llm`

3. **`haystack`**  
   - Description : Un framework open-source pour la recherche d’informations et la génération de réponses, basé sur des documents (retrieval-augmented generation).  
   - Use-case : Rechercher des sources et des documents pour confirmer ou infirmer une affirmation.  
   - Installation : `pip install farm-haystack`  
   - [GitHub](https://github.com/deepset-ai/haystack)

4. **`fact-checker`**  
   - Description : Un package expérimental pour automatiser la vérification de faits en utilisant des règles ou des modèles ML.  
   - Installation : `pip install fact-checker`  
   - [GitHub](https://github.com/soroushchehresa/fact-checker)

5. **`transformers` (Hugging Face)**  
   - Description : Permet de travailler avec des modèles de langage pré-entraînés pour l'extraction d'informations, la génération ou la comparaison de faits.  
   - Use-case : Utiliser des modèles comme `BART`, `T5`, ou des LLMs pour reformuler ou fact-checker des affirmations.  
   - Installation : `pip install transformers`  
   - Exemple : [BART](https://huggingface.co/facebook/bart-large-cnn) pour la synthèse et la comparaison.

6. **`openai` API (GPT-4)**  
   - Description : Les modèles GPT peuvent être utilisés pour reformuler des affirmations et les comparer avec des sources existantes.  
   - Use-case : Automatiser des pipelines de vérification en analysant des affirmations.

7. **`pandas` + `fuzzywuzzy` ou `rapidfuzz`**  
   - Description : Combine des outils de traitement de données et des algorithmes de recherche floue pour vérifier la similarité entre les faits extraits et les bases de données de vérités.  
   - Installation : `pip install pandas rapidfuzz`

---

## **Approches avancées pour le fact-checking :**

1. **`LangChain`**  
   - Framework pour intégrer des modèles LLM et des sources externes (par ex., une base de données ou des API) pour créer un agent capable de vérifier des faits.  
   - Installation : `pip install langchain`  
   - [LangChain GitHub](https://github.com/langchain-ai/langchain)

2. **Récupération augmentée (RAG)**  
   - Approche utilisant des modèles comme GPT-4 en combinaison avec des moteurs de recherche ou des documents pour générer des réponses précises avec des références.

3. **`llama_index` (ex-`GPT Index`)**  
   - Pour structurer des bases de connaissances locales afin de les interroger avec un modèle de langage.  
   - Installation : `pip install llama-index`  
   - [GitHub](https://github.com/jerryjliu/llama_index)

---

Si tu veux une **démo de pipeline complet** combinant plusieurs outils (extraction avec `newsplease` + vérification via `transformers` ou `langchain`), fais-le-moi savoir. 🚀


