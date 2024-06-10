# ia_all_prompts_2.md

---

# Introduction

1. **Ces `Prompts` sont issus soit d'ateliers, soit de recherche, soit de création en fonction de cas d'usage précis... Ces `Prompts` constituent le socle de la `Prompt Academy`. Afin de faciliter la compréhension de chacun, si vous êtes familier de l'agilité et donc de la `User Story`. On peut convenir que le `Prompt` est très proche du concept de `User Story`. Le `Prompt` décrit une fonctionnalité qui va être exécutée par l'IA (Intelligence Artificielle).**

2. **Il s'agit de la totalité des prompts utilisés par le dispositif plus quelques ressources additionnelles.**

3. **Les principaux acronymes utilisés  et leurs définitions :** 
	+ **SEO (Search Engine Optimization) :** Référencement naturel (optimisation pour les moteurs de recherche)
	+ **SMO (Social Media Optimisation) :** Optimisation des médias sociaux (stratégies pour améliorer la visibilité et l'engagement sur les réseaux sociaux)
	+ **ASO (App Store Optimization) :** Optimisation pour les magasins d'applications (techniques pour améliorer la visibilité et le téléchargement d'une application dans les magasins d'applications)
	+ **LLM (Large Language Model) :** LLM signifie "Grand modèle de langage" (Large Language Model) en français. Il s'agit d'un modèle informatique de traitement automatique du langage naturel capable de comprendre et de générer du texte dans une ou plusieurs langues, en utilisant des techniques d'apprentissage profond (deep learning) pour analyser de vastes corpus de données textuelles. Les LLM sont utilisés dans de nombreuses applications, telles que la traduction automatique, la réponse aux questions, la génération de texte, et l'analyse de sentiment. Par exemple : ChatGPT 3.5 turbo, Mistral Small, Phi-3 sont des LLM.
	+ **NLP (Natural Language Processing) :** NLP  signifie "Traitement automatique du langage naturel" (Natural Language Processing) en français. Il s'agit d'un domaine de recherche interdisciplinaire qui vise à développer des systèmes informatiques capables de comprendre, d'interpréter et de générer du langage naturel, c'est-à-dire le langage humain tel qu'il est parlé ou écrit dans la vie courante. Le NLP s'appuie sur des techniques issues de l'informatique, de la linguistique, de la statistique et de l'apprentissage automatique (machine learning) pour analyser et traiter des données textuelles ou vocales. Les applications du NLP sont nombreuses et variées, allant de la traduction automatique à la reconnaissance vocale, en passant par la synthèse vocale, l'analyse de sentiment, la recherche d'information, la correction grammaticale, etc.

---

# Qu'est une User Story et un Prompt ? (`User Story` vs `Prompt`)

Le prompt est proche de la User Story agile dans la mesure où ils sont tous deux utilisés pour définir les besoins et les attentes d'un utilisateur ou d'un client.

Voici quelques points de convergence entre le prompt et la User Story agile :

* Ils sont tous deux centrés sur l'utilisateur ou le client, et cherchent à comprendre ses besoins et ses attentes.
* Ils sont tous deux formulés de manière simple et concise, afin de faciliter la compréhension et la communication.
* Ils sont tous deux utilisés pour guider le développement d'un produit ou d'un service, en fournissant des indications sur les fonctionnalités à implémenter et les résultats à atteindre.

Cependant, il existe également des points de divergence entre le prompt et la User Story agile. Voici quelques exemples :

* La User Story agile est généralement plus détaillée que le prompt, et comprend des informations supplémentaires telles que les critères d'acceptation, les contraintes et les dépendances.
* La User Story agile est généralement écrite du point de vue de l'utilisateur ou du client, tandis que le prompt peut être formulé de différentes manières, en fonction de l'objectif et du contexte.
* La User Story agile est généralement utilisée dans le cadre d'une méthodologie agile, telle que Scrum ou Kanban, tandis que le prompt peut être utilisé dans des contextes plus variés, tels que la rédaction de contenu, la génération d'idées ou la recherche d'informations.

En résumé, le prompt et la User Story agile sont deux outils différents mais complémentaires pour définir les besoins et les attentes des utilisateurs ou des clients, et pour guider le développement de produits ou de services qui répondent à ces besoins et attentes.


---

# Collection


<!-- 001_seo_prompts.csv -->

## 1. PROMPT SEO PART_1

**Il s'agit d'un premier jeu de prompts basé sur les premières expressions de besoin en matière de SEO.**


### PROMPT SEO #1
- **Objectif :** Depuis un contenu en ANGLAIS, générer 3 titres et 3 mots-clés en ANGLAIS
- **Nom technique :** `english_seo_prompt` 

```text
You are a smart and intelligent journalist. Craft three compelling and unique titles for an online post about the topic given in the content. Ensure to incorporate SEO best practices by including the most common and relevant keywords from the content in each title. For each proposal, print only the result in a Python dictionary object with 'title' as a string and 'keywords' as a list. Include all three results into a Python list object like defined below. Output Format:[{{"title": "The value of the title", "keywords": ["keyword1", "keyword2", "keyword3"]}}, {{"title": "The value of the title", "keywords": ["keyword1", "keyword2", "keyword4"]}}, {{"title": "The value of the title", "keywords":["keyword1", "keyword2", "keyword5"]}}] Content: '{content}'

```
### PROMPT SEO #2

**Objectif:** 
Depuis un contenu en FRANCAIS, générer 3 titres et 3 mots-clés en FRANCAIS

**Nom technique:** `french_seo_prompt` 

```text
You are a French smart and intelligent journalist. Craft three compelling titles in French for an online post about the topic given in the content in French. Ensure to incorporate SEO best practices by including the most common keywords from the content. For each proposal, print only the result in French as a Python dictionary object with 'title' as a string and 'keywords' as a list. Include all results into a Python list object as defined below. Output Format:[ {{"title": "The value of the title", "keywords": ["keyword1", "keyword2", "keyword3"]}}, {{"title": "The value of the title", "keywords": ["keyword1", "keyword2", "keyword3"]}}, {{"title": "The value of the title", "keywords": ["keyword1", "keyword2", "keyword3"]}}] Content: '{content}'

```

---

<!-- 002_smo_prompts.csv -->
## 2. PROMPT SMO

**Il s'agit d'un deuxième jeu de prompts basé sur les ateliers SEO menés au sein des rédactions pour sensibiliser les journalistes aux problématiques SEO.**


### PROMPT SMO #1
**Objectif:** 
Depuis un contenu en ANGLAIS, générer 3 tweets de 280 caractéres et 3 hashtags en ANGLAIS

**Nom technique:** `english_smo_prompt` 



```text
You are a smart and intelligent community manager. Craft three compelling messages of 280 characters each for an online post about the topic given in the content. Ensure to incorporate Social Media Optimization (SMO) best practices by including the most common keywords from the content. For each proposal, print only the result in a Python dictionary object with 'message' as a string and 'hashtags' as a list of hashtags. In the list of hashtags, for each hashtag, do not forget to add the sign "#" in front of it e.g. "hashtags": ["#hashtag1", "#hashtag2", "#hashtag3"]. Include all results into a Python list object as defined below. Output Format:[{{"message": "The value of the message", "hashtags": ["#hashtag1", "#hashtag2", "#hashtag3"]}}, {{"message": "The value of the message", "hashtags": ["#hashtag1", "#hashtag2", "#hashtag3"]}}, {{"message": "The value of the message", "hashtags": ["#hashtag1", "#hashtag2", "#hashtag3"]}}] Content: '{content}'
```

### PROMPT SMO #2
**Objectif:** 
Depuis un contenu en FRANCAIS, générer 3 tweets de 280 caractéres et 3 hashtags en FRANCAIS

**Nom technique:** `french_smo_prompt` 


```text
En français, vous êtes un gestionnaire de communauté intelligent et futé. Rédigez en français trois messages percutants de 280 caractères chacun pour une publication en ligne sur le sujet donné dans le contenu, en veillant à incorporer les meilleures pratiques d'optimisation des médias sociaux (SMO) avec les mots-clés les plus courants du contenu. Pour chaque proposition en français, n'imprimez que le résultat dans un objet Python dictionary avec 'message' sous forme de chaîne et 'hashtags' sous forme de liste de hashtags. Dans la liste des hashtags, pour chaque hashtag, n'oubliez pas d'ajouter le signe "#" devant celui-ci, par exemple "hashtags": ["#hashtag1", "#hashtag2", "#hashtag3"]. Incluez tous les résultats dans un objet Python list comme défini ci-dessous. Format de Sortie: [ {{"message": "La valeur du message", "hashtags": ["#hashtag1", "#hashtag2", "#hashtag3"]}}, {{"message": "La valeur du message", "hashtags": ["#hashtag1", "#hashtag2", "#hashtag3"]}}, {{"message": "La valeur du message", "hashtags": ["#hashtag1", "#hashtag2", "#hashtag3"]}}] Contenu: '{content}'
```

### PROMPT SMO #3
**Objectif:** 
Depuis un texte en FRANCAIS, générer un message de 150 à 300 caractères + entités (pays, villes, états, pays) + emoji de drapeau

**Nom technique:** `french_smo_prompt_emoji` 


```text
En français, vous êtes un gestionnaire de communauté intelligent et futé. Rédigez en français un message attractif editorialement qui comprend environ de 150 à 300 caractères  pour une publication en ligne sur le sujet donné dans le contenu. Pour ce message, il faut veiller à incorporer les meilleures pratiques d'optimisation des médias sociaux (SMO). Si le message généré contient des entités notamment les "GPE" ou Entité géopolitique, c'est-à-dire pays, villes, États, il faut transformer l'entité en hashtag et ajouter quand c'est possible l'emoji du drapeau du pays par exemple. Il faut enfin ajouter un hashtag pour le fait editorialement saillant dans le sujet donné dans le contenu. Dans le message, tous les hashtags et les emojis doivent être ajoutés dans le sens de la lecture c'est à dire ni en fin de proposition ni en début de proposition. Pour chaque proposition en français, n'imprimez que le résultat dans un objet Python dictionary avec 'message' sous forme de chaîne contenant les hashtags et les emojis comme indiqué plus haut, 'hashtags' sous forme de liste de hashtags et 'emojis' sous forme de liste de emojis. Dans la liste des hashtags, pour chaque hashtag, n'oubliez pas d'ajouter le signe "#" devant celui-ci, par exemple "hashtags": ["#hashtag1", "#hashtag2", "#hashtag3"]. Dans la liste des emojis, pour chaque emoji, voilà un exemple "emojis": ["emoji1", "emoji2", "emoji3"]. Incluez tous les résultats dans un objet Python list comme défini ci-dessous. Format de Sortie:\n [{{"message": "La valeur du message avec les hashtags et les emojis", "hashtags": ["#hashtag1", "#hashtag2", "#hashtag3"], "emojis": ["emoji1", "emoji2", "emoji3"]}}] Contenu: '{content}'
```

---

## 3. PROMPT SEO PART_2

**Un jeu de prompt dédiés au SEO sur la base des ateliers dispensés aux rédactions pour les sensibiliser aux problématiques du SEO.**


<!-- 003_seo_prompts_workshops.csv -->

### PROMPT WORKSHOP SEO #1
**Objectif:** 
Générer 10 suggestions de titres pour un contenu

**Nom technique:** `seo_manage_title`

```text
As an SEO and IA expert, could you please generate 10 engaging and SEO-friendly headline suggestions for an online post about the topic given in the content ensuring to incorporate SEO best practices. The headlines should be in the same language as the post. To ensure the output is in the correct format, please provide for each headline as a string within a Python dictionary object, with 'headline' as the key. All of these dictionaries should then be included in a Python list object. Please ensure that you replace 'Headline1', 'Headline2', and so on with the actual headlines you generate.Output Format: [{{"headline": "The value of the Headline1"}}, {{"headline": "The value of the Headline2"}}, {{"headline": "The value of the Headline3"}}, {{"headline": "The value of the Headline4"}}, {{"headline": "The value of the Headline5"}}, {{"headline": "The value of the Headline6"}}, {{"headline": "The value of the Headline7"}}, {{"headline": "The value of the Headline8"}}, {{"headline": "The value of the Headline9"}}, {{"headline": "The value of the Headline10"}}] Content: '{content}'
```

### PROMPT WORKSHOP SEO #2
**Objectif:** 
Générer 10 URLs optimisées pour un contenu

**Nom technique:** `seo_manage_url` 

```text
As an SEO and Information Architecture (IA) expert, generate 10 SEO-friendly URLs for an online post about the topic given in the content ensuring to incorporate SEO best practices. The URLs should be in the same language as the post and should be compelling, relevant, and keyword-optimized. To ensure the output is correctly formatted, please provide each URL as a string within a Python dictionary object, with 'url' as the key. All of these dictionaries should then be included in a Python list object. Please replace 'url1', 'url2', and so on with the actual URLs you generate. Remember to use hyphens (-) to separate words in the URLs, and avoid using special characters or spaces. Output Format: [ {{"url": "The value of the url1"}}, {{"url": "The value of the url2"}}, {{"url": "The value of the url3"}}, {{"url": "The value of the url4"}}, {{"url": "The value of the url5"}}, {{"url": "The value of the url6"}}, {{"url": "The value of the url7"}}, {{"url": "The value of the url8"}}, {{"url": "The value of the url9"}}, {{"url": "The value of the url10"}}] Content: '{content}'
```

### PROMPT WORKSHOP SEO #3
**Objectif:** 
Générer une meta-description pour un contenu

**Nom technique:** `seo_manage_meta_description`

```text
As an SEO and Information Architecture (IA) expert, craft a compelling and concise meta description for an online post about the topic given in the content ensuring to incorporate SEO best practices. The meta description should be in the same language as the post, and it should accurately summarize the content of the post while also enticing users to click through to the post. The meta description should be between 150 and 160 characters in length, including spaces. Please replace 'meta description text' with the actual meta description you generate. Be sure to enclose the meta description in quotation marks and to check that it meets the character length requirements. Output Format: [{{"meta_description": "meta description text"}}] Content: '{content}'

```

### PROMPT WORKSHOP SEO #4
**Objectif:** 
Générer 10 étiquettes de lien (link labels) pour un contenu

**Nom technique:** `seo_manage_label_internal_link`

```text
As an SEO and Information Architecture (IA) expert, generate 10 semantically meaningful and editorial-friendly link labels for an online post about the topic given in the content ensuring to incorporate SEO best practices. The link labels should be in the same language as the post and should accurately describe the content that the link will point to. To ensure the output is correctly formatted, please provide each link label as a string within a Python dictionary object, with 'linklabel' as the key. All of these dictionaries should then be included in a Python list object. Please replace 'label1', 'label2', and so on with the actual link labels you generate. Remember to use descriptive and concise language for the link labels, and to avoid using generic phrases like 'click here' or 'read more'. Output Format: [ {{"linklabel": "label1"}},{{"linklabel": "label2"}}, {{"linklabel": "label3"}}, {{"linklabel": "label4"}}, {{"linklabel": "label5"}}, {{"linklabel": "label6"}}, {{"linklabel": "label7"}}, {{"linklabel": "label8"}}, {{"linklabel": "label9"}}, {{"linklabel": "label10"}} ] Content: '{content}'
```

### PROMPT WORKSHOP SEO #5
**Objectif:** 
Effectuer une reconnaissance d'entités nommées pour un contenu

**Nom technique:** `seo_manage_ner_tags`

```text
Given the input text: '{content}', perform Named Entity Recognition (NER) detection on it.The following NER tags should be used: FAC, CARDINAL, NUMBER, DEMONYM, QUANTITY, TITLE, PHONE_NUMBER, NATIONAL, JOB, PERSON, LOC, NORP, TIME, CITY, EMAIL, GPE, LANGUAGE, PRODUCT, ZIP_CODE, ADDRESS, MONEY, ORDINAL, DATE, EVENT, CRIMINAL_CHARGE, STATE_OR_PROVINCE, RELIGION, DURATION, WORK_OF_ART, PERCENT, CAUSE_OF_DEATH, COUNTRY, ORG, LAW, NAME, COUNTRY, RELIGION, TIME. The answer must be in the format tag:value, where 'tag' is the NER tag and 'value' is the corresponding entity value. Each tag-value pair should be included in a JSON dictionary object, and all of these dictionaries should then be included in a JSON list object. Output Format: [ {{"tag": "tag1", "value": "value1"}},{{"tag": "tag2", "value": "value2"}}, {{"tag": "tag3", "value": "value3"}}, ...]Please replace 'tag1', 'tag2', and so on with the actual NER tags you detect, and 'value1', 'value2', and so on with the corresponding entity values.Note: If no entities are detected in the input text, please return an empty list in JSON format: [].
```

### PROMPT WORKSHOP SEO #6
**Objectif:** 
Générer une structure de code HTML pour un contenu

**Nom technique:** `seo_manage_html_subtitles`


```text
As an SEO and Information Architecture (IA) expert, please generate an HTML code structure for the post content: '{content}' in the same language as the post. The HTML code should use <H1>, <H2>, and <H3> tags to effectively organize the content and improve its readability. The structure should also follow best SEO practices for optimal search engine optimization. To ensure the output is correctly formatted, please provide the HTML code as a string within a JSON dictionary object, with 'html_structure' as the key. Output Format: [{{"html_structure": "<H1>Title</H1><H2>Subtitle1</H2><p>Content1</p><H2>Subtitle2</H2><p>Content2</p><H3>Sub-subtitle1</H3><p>Content3</p><H3>Sub-subtitle2</H3><p>Content4</p>" }} ] Please replace the example HTML code with the actual HTML code you generate. Be sure to enclose the HTML code in quotation marks and to check that it meets the requirements for effective content organization and SEO optimization. Note: If the content provided does not have enough information to create a structure with <H1>, <H2>, and <H3> tags, please return a JSON dictionary object with an empty string as the value for the 'html_structure' key: {{"html_structure": ""}}.
```

### PROMPT WORKSHOP SEO #7
**Objectif:** 
Générer 10 descriptions de texte alternatif (alt text) pour un contenu

**Nom technique:** `seo_manage_image_alt_attribute`

```text
As an SEO and Information Architecture (IA) expert, please generate 10 alt text descriptions in the same language as the post for images related to the main topic of the post: '{content}' in the same language as the post. Each alt text should be in the same language as the post. Each alt text should incorporate synonyms or variations of the main keyword and should accurately describe the image. The alt text should also be concise and should not exceed 125 characters, including spaces. To ensure the output is correctly formatted, please provide each alt text description as a string within a JSON dictionary object, with 'alt_text' as the key. All of these dictionaries should then be included in a JSON list object. Output Format: [ {{"alt_text": "alt text description 1"}}, {{"alt_text": "alt text description 2"}}, {{"alt_text": "alt text description 3"}}, ... ] Please replace 'alt text description 1', 'alt text description 2', and so on with the actual alt text descriptions you generate. Be sure to enclose the alt text descriptions in quotation marks and to check that they meet the requirements for accuracy, conciseness, and character length. Note: If the main topic of the post does not have enough related images to generate 10 alt text descriptions, please return a JSON list object with the number of alt text descriptions that were generated.

```

--- 

<!-- 004_summary_prompts.csv -->

**Un jeu de prompts dédiés au résumé depuis un texte existant. Attention, les LMM peuvent servir de traducteur lors d’un résumé même si toutes les langues ne sont pas comprises par le LLM. C’est une alternative possible à des LLM entraînés spécialement pour cette fonction de traduction comme NLLB (No Language Left Behind)**


## 4. PROMPT SUMMARY

**Un jeu de prompt dédiés au résumé depuis un texte existant.**


### PROMPT SUMMARY #1
**Objectif:** 
Depuis un texte en ANGLAIS, faire un résumé en ANGLAIS

**Nom technique:** `english_summarize_prompt`


```text
You are a helpful summarizer assistant in English. Your task is to generate a valid summary object in English based on the given information. Content: '{content}'. You should also identify 5 keywords or phrases that best represent the content. For the proposal, print only the result in a Python dictionary object with the summary as a string and the 5 keywords as a list. Include the all result into a Python list object like define below. Output Format: [ {{"summary": "The summary of the content", "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"] }} ]
```

### PROMPT SUMMARY #2
**Objectif:** 
Depuis un texte en FRANÇAIS, faire un résumé en FRANÇAIS

**Nom technique:** `french_summarize_prompt`

```text
You are a helpful summarizer assistant in French. Your task is to generate a valid summary object in French based on the given information. Content: '{content}'. You should also identify 5 keywords or phrases that best represent the content. For the proposal, print only the result in a Python dictionary object with the summary as a string and the 5 keywords as a list. Include the all result into a Python list object like define below. Output Format: [ {{"summary": "The summary of the content", "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"] }} ]
```

### PROMPT SUMMARY #3
**Objectif:** 
Générer le résumé dans une langue, sans longueur spécifique

**Nom technique:** `text_summarize_no_length`

```text
Given the input text in '{language}': Input: '{content}' Produce a summary of the text in '{language}'. The summary must be in the same language from the original text in '{language}'. Captures the main ideas and key points of the text. Summary Does not include verbatim sentences from the original text. For the proposal, print only the result in a Python dictionary object with the summary as a string. Include the all result into a Python list object like define below. Output Format: [ {{"summary": "The summary of the content"}}]
```

### PROMPT SUMMARY #4
**Objectif:** 
Générer le résumé dans une langue avec une longueur spécifique

**Nom technique:** `text_summarize`

```text
Given the input text in '{language}': Input: '{content}' Produce a '{summary_length}' sentences length summary of the text in '{language}'. The summary must be in the same language from the original text in '{language}'. Captures the main ideas and key points of the text. Summary Does not include verbatim sentences from the original text. For the proposal, print only the result in a Python dictionary object with the summary as a string and the summary_length keywords as a integer. Include the all result into a Python list object like define below. Output Format: [ {{"summary": "The summary of the content", "summary_length": summary_length_number }}]

```

--- 

## 5. PROMPT TRANSLATION

<!-- 005_translation_prompts.csv -->

**Un jeu de prompts dédiés à la traduction depuis un texte existant. Attention, les LMM peuvent servir de traducteur même si toutes les langues ne sont pas comprises par le LLM. C’est un alternative possible à des LLM entraînés spécialement pour cette fonction de traduction comme NLLB (No Language Left Behind)**

### PROMPT TRANSLATION #1
**Objectif:** 
Depuis un texte en ANGLAIS, faire une traduction en FRANÇAIS


**Nom technique:** `english_to_french_translate_prompt`
```text
You are a helpful and accurate translator. You have been provided with a source text in English, and your task is to translate this text into French. Please ensure that the translation preserves the original meaning and context as closely as possible. English Source Text: '{content}' French Translation:
```

### PROMPT TRANSLATION #2
**Objectif:** 
Depuis un texte en FRANÇAIS, faire une traduction en FRANÇAIS

**Nom technique:** `french_to_english_translate_prompt`

```text
You are a helpful and accurate translator. You have been provided with a source text in French, and your task is to translate this text into English. Please ensure that the translation preserves the original meaning and context as closely as possible. French Source Text: '{content}' English Translation:

```

--- 

## 6. PROMPT DATA

**Ces prompts sont uniquement à destination de la DATA. Ces prompts sont uniquement à destination de la DATA. Ils ont pas comme première vocation à fournir non une proposition éditoriale pour un journaliste mais  un traitement purement fonctionnel pour faciliter la compréhension d'éléments statistiques.**


<!-- 006_dera_prompts.csv -->

### PROMPT DATA #1
**Objectif:** 
Proposer une catégorisation définie du contenu

**Nom technique:** `dera_choice_cat_defined_prompt`

```text
Act as a highly intelligent news chatbot and classify the given news text into one of the following categories only: France, Europe, Africa, America, Asia-Pacific, Middle East, Sports, Economy, Technology, Culture, Environment. Do not code. Return only one word answer with only the category name that the given news text belongs to. In the output, return the result in a field named ""category_predicted:"" and return the comment in the field ""category_decision:"" in a python Dictionary. News text: '{content}'?
```

### PROMPT DATA #2
**Objectif:** 
Proposer une catégorisation libre du contenu

**Nom technique:** `dera_choice_cat_prompt`

```text
Act as a highly intelligent news chatbot and classify the given news text into the most adequate single category. Do not code. Return only one word answer with only the category name that the given news text belongs to. In the output, return the result in a field named ""category_predicted:"" and return the comment in the field ""category_decision:"" in a python Dictionary. News text: '{content}'?

```

---

<!-- 007_aso_prompts.csv -->

## 7. PROMPT ASO

**Ces prompts sont uniquement à destination des P.O des APPS afin d'améliorer la stratégie ASO (App Store Optimization).  L'objectif d'une stratégie ASO (App Store Optimization) est d'augmenter la visibilité et le nombre de téléchargements de l'application.**




### PROMPT ASO #1
**Objectif:** 
Uniquement pour les P.O des APPS, Générer 10 titres d'application selon des recommandations ASO. Plusieurs paramètres sont à compléter. Un exemple est donné dans la colonne exemple et ci-dessous un exemple des valeurs à passer dans les paramètres.

- aso_app_main_language e.g. `'French'`
- aso_app_main_os e.g. `'iOS'`
- aso_app_primary_keywords e.g. `'actualité en direct, application France 24, contenus exclusifs, journalistes de France 24, articles, reportages, émissions, vidéos, français, anglais, espagnol, arabe, naviguer facilement, multimédias, partage sur les réseaux sociaux, info en continu, 24h/24 et 7j/7, faits-divers, grands événements internationaux, actualités françaises et internationales, rubriques spécialisées, Afrique, Moyen-Orient, Eco-Tech, Découvertes, replay vidéo, journaux sous-titrés, magazines de la rédaction, réseaux sociaux, Facebook, Twitter, Instagram, TikTok, YouTube, Telegram, Soundcloud, donnez-nous une note, laissez-nous un commentaire, France Médias Monde, Radio France Internationale, Monte Carlo Doualiya'`
- aso_app_brand_name e.g. `'FRANCE 24'`
 

**Nom technique:** `aso_title_optimization`

```text
As an ASO expert, could you generate 10 engaging application titles in '{aso_app_main_language}' for a mobile app on '{aso_app_main_os}'? Please adhere to these guidelines: 1. Limit titles to 30 characters for proper display on all devices. 2. Include primary keywords that users are likely to search for: '{aso_app_primary_keywords}'. 3. Make sure to incorporate your brand name: '{aso_app_brand_name}'.","Attention le prompt comprend pas mal de variable afin de la rendre utilisable pour différentes combinaisons de marque, de langue et d’OS notamment","As an ASO expert, could you generate 10 engaging application titles in 'FR' for a mobile app on 'iOS'? Please adhere to these guidelines: 1. Limit titles to 30 characters for proper display on all devices. 2. Include primary keywords that users are likely to search for: 'actualité en direct, application France 24, contenus exclusifs, journalistes de France 24, articles, reportages, émissions, vidéos, français, anglais, espagnol, arabe, naviguer facilement, multimédias, partage sur les réseaux sociaux, info en continu, 24h/24 et 7j/7, faits-divers, grands événements internationaux, actualités françaises et internationales, rubriques spécialisées, Afrique, Moyen-Orient, Eco-Tech, Découvertes, replay vidéo, journaux sous-titrés, magazines de la rédaction, réseaux sociaux, Facebook, Twitter, Instagram, TikTok, YouTube, Telegram, Soundcloud, donnez-nous une note, laissez-nous un commentaire, France Médias Monde, Radio France Internationale, Monte Carlo Doualiya'. 3. Make sure to incorporate your brand name: 'FRANCE 24'.
```

### PROMPT ASO #2
**Objectif:** 
Uniquement pour les P.O des APPS, générer 10 sous-titres d'application selon des recommandations ASO. Plusieurs paramètres sont à compléter. Un exemple est donné dans la colonne exemple et ci-dessous un exemple des valeurs à passer dans les paramètres.

- aso_app_main_language e.g. `'French'`
- aso_app_main_os e.g. `'ANDROID'`
- aso_app_subtitle e.g. `'RFI - L'actualité mondiale. Articles, reportages, émissions, radio en direct et à la demande, alertes - tous les contenus de RFI sur l'actualité française, africaine et internationale à portée de main sur tous vos appareils.'`
- aso_app_brand_name e.g. `'RFI'`

**Nom technique:** `aso_subtitle_optimization`

```text
As an experienced ASO (App Store Optimization) specialist, please generate 10 engaging application subtitles in '{aso_app_main_language}' for a mobile app on '{aso_app_main_os}', incorporating '{aso_app_subtitle}'. To ensure diversity, use synonyms or variations of the primary keywords and include your brand name '{aso_app_brand_name}'. Please strictly adhere to the 30-character limit for subtitles to comply with the App Store guidelines.","Attention le prompt comprend pas mal de variable afin de la rendre utilisable pour différentes combinaisons de marque, de langue et d’OS notamment","As an experienced ASO (App Store Optimization) specialist, please generate 10 engaging application subtitles in 'FR' for a mobile app on 'ANDROID', incorporating 'RFI - L'actualité mondiale. Articles, reportages, émissions, radio en direct et à la demande, alertes - tous les contenus de RFI sur l'actualité française, africaine et internationale à portée de main sur tous vos appareils.'. To ensure diversity, use synonyms or variations of the primary keywords and include your brand name 'RFI'. Please strictly adhere to the 30-character limit for subtitles to comply with the App Store guidelines.
```

### PROMPT ASO #3
**Objectif:** 
Uniquement pour les P.O des APPS, faire une extraction des 50 meilleurs mots-clés dans la même langue que le contenu ci-dessous. Cela produit une liste de mots-clés dans un format de liste séparé par des virgules pour faciliter le copier-coller. Attention au texte inséré dans le prompt saut de ligne, caractères spéciaux... 

- aso_blob_text e.g `texte copié-collé depuis les pages des applications mobiles concurrentes`

**Nom technique:** `aso_keywords_extraction`

```text
As an expert in SEO and ASO, please extract from the content below the top 50 keywords with the same language. List the keywords with in a comma-separeted list to ease the cut and paste like output format: [""keyword1"", ""keyword2"", ""keyword3""...]. The content is the following. Content: '{aso_blob_text}' as a reference. The keywords should be based on the most frequently used terms in the descriptions of the top three apps in this category.",Idem,"
As an expert in SEO and ASO, please extract from the content below the top 50 keywords. List the keywords with in a comma-separeted list to ease the cut and paste like output format: [""keyword1"", ""keyword2"", ""keyword3""...]. The content is the following. Content: 'Google Actualités est un agrégateur qui organise et met en avant de façon personnalisée les informations du monde entier pour vous permettre de vous tenir rapidement aux courants des actualités et d'en savoir plus sur les sujets qui vous intéressent vraiment. 

- ""Le Monde"" lance la version audio de ses articles.

Nous franchissons ainsi une nouvelle étape dans notre ambition de s’adapter aux nouveaux usages. En voiture, dans le métro ou pendant un footing, l’information de qualité reste accessible. - Une seule application pour découvrir l'actualité en direct et l'intégralité du quotidien dès 11h, ainsi que les cahiers hebdomadaires, les suppléments mensuels et les hors séries.


```

### PROMPT ASO #4
**Objectif:** 
Uniquement pour les P.O des APPS, générer une description d'application dans une langue principale pour une application mobile en utilisant des exemples comme source d'inspiration. Veillez à intégrer des mots-clés pertinents et à inclure le nom de votre marque.

- aso_app_main_language e.g. `'French'`
- aso_app_brand_name e.g. `'FRANCE 24'`
- aso_app_main_os e.g. `'iOS'`

- user_input e.g. 
`1. TF1 INFO - LCI: Actualités La Chaine Info Découvrez toute l'actualité en direct avec TF1 INFO - LCI. Suivez les dernières nouvelles en France et à l'international, les reportages exclusifs, les analyses et les vidéos. Recevez des alertes pour rester informé en temps réel. L'info en continu, à portée de main.2. Google Actualités Google Actualités vous propose une couverture complète et personnalisée des actualités qui vous intéressent. Explorez les articles des plus grandes publications et recevez des alertes sur les sujets de votre choix. Restez informé grâce à des mises à jour en temps réel et à une sélection de sources fiables. 3. Le Monde, Live, Actu en direct
Retrouvez toute l'actualité avec Le Monde. Accédez à des articles en profondeur, des analyses, des vidéos et des photos. Suivez les événements en direct et recevez des notifications sur les sujets qui vous intéressent. Une couverture complète de l'actualité française et internationale, 24h/24.
`

**Nom technique:** `aso_engaging_app_descriptions`

```text
As an ASO (App Store Optimization) expert proficient, could you write a compelling application description in '{aso_app_main_language}' for an '{aso_app_main_os}' mobile application, using the following examples as a source of inspiration? Incorporate relevant keywords and ensure your brand name is '{aso_app_brand_name}'.

Here are the examples:

{user_input}

Please make sure to write a unique and engaging description that highlights the features and benefits of your app, while also incorporating the best practices and strategies from the examples provided.",Idem,"As an ASO (App Store Optimization) expert proficient, could you write a compelling application description in 'French' for an 'iOS' mobile application, using the following examples as a source of inspiration? Incorporate relevant keywords and ensure your brand name is 'FRANCE 24'.

Here are the examples:

'1. TF1 INFO - LCI: Actualités La Chaine Info
Découvrez toute l'actualité en direct avec TF1 INFO - LCI. Suivez les dernières nouvelles en France et à l'international, les reportages exclusifs, les analyses et les vidéos. Recevez des alertes pour rester informé en temps réel. L'info en continu, à portée de main.

2. Google Actualités
Google Actualités vous propose une couverture complète et personnalisée des actualités qui vous intéressent. Explorez les articles des plus grandes publications et recevez des alertes sur les sujets de votre choix. Restez informé grâce à des mises à jour en temps réel et à une sélection de sources fiables.

3. Le Monde, Live, Actu en direct
Retrouvez toute l'actualité avec Le Monde. Accédez à des articles en profondeur, des analyses, des vidéos et des photos. Suivez les événements en direct et recevez des notifications sur les sujets qui vous intéressent. Une couverture complète de l'actualité française et internationale, 24h/24.'

Please make sure to write a unique and engaging description that highlights the features and benefits of your app, while also incorporating the best practices and strategies from the examples provided.

```

### PROMPT ASO #5
**Objectif:** 
Uniquement pour les P.O des APPS, ce prompt est une instruction pour générer les 50 meilleurs mots-clés pour une application mobile basé sur une user-story et des objectifs utilisateurs.

A titre d'exmple le contexte fourni indique que l'application en question est une application de productivité dans la catégorie Business. Le public cible est composé de professionnels occupés qui ont besoin de gérer leurs tâches et leur temps efficacement. L'objectif de la stratégie ASO (App Store Optimization) est d'augmenter la visibilité et le nombre de téléchargements de l'application.

**ATTENTION : bien modifier à la fois la user story et les objectifs poursuivis**


Les attentes définissent le format de sortie souhaité, à savoir une liste de mots-clés séparés par des virgules. Il est également précisé que les mots-clés doivent être en minuscules et sans ponctuation. Les mots-clés doivent être basés sur les termes les plus fréquemment utilisés dans les descriptions des trois meilleures applications de cette catégorie. L'accent doit être mis sur les fonctionnalités uniques et les avantages de l'application ex: la gestion des tâches, le suivi du temps et la réduction du stress.

Enfin, il est précisé que des éclaircissements peuvent être demandés si nécessaire et que des suggestions pour améliorer le contenu ou les mots-clés sont les bienvenues.

**Nom technique:** `aso_generate_keywords_abstract`


**EXEMPLE_1 : Prompt pour une app de productivité**

```text

Instruction: Generate the top 50 keywords for a mobile application.

Background: The content is for a productivity app in the Business category. The target audience is busy professionals who need to manage their tasks and time effectively. The goal of the ASO strategy is to increase the visibility and the downloads of the app.

Expectations:

* List the keywords in a comma-separated format, like this: ""keyword1, keyword2, keyword3"".
* Use lowercase letters and no punctuation, like this: ""productivity"" not ""Productivity!""
* Base the keywords on the most frequently used terms in the descriptions of the top three apps in this category.
* Focus on the unique features and the benefits of the app, such as ""task management"", ""time tracking"", and ""stress reduction"".

Output: [""keyword1"", ""keyword2"", ""keyword3""...]

Note: Feel free to ask for clarification if needed, and let me know if you have any suggestions for improving the content or the keywords."
```

**EXEMPLE_2 : Prompt pour une app de news international**

```text
Instruction: Generate the top 50 keywords for a mobile application.

Background: The content is for a news app in the News & Magazines category. The target audience is people who want to stay informed about international news from various sources. The goal of the ASO strategy is to increase the app's visibility and attract users who are looking for a comprehensive and unbiased news source.

Expectations:

* List the keywords in a comma-separated format, like this: ""keyword1, keyword2, keyword3"".
* Use lowercase letters and no punctuation, like this: ""news"" not ""News!""
* Base the keywords on the most frequently used terms in the descriptions of the top three apps in this category.
* Focus on the unique features and the benefits of the app, such as ""comprehensive news"", ""unbiased reporting"", and ""multiple sources"".

Output: [""keyword1"", ""keyword2"", ""keyword3""...]

Note: Feel free to ask for clarification if needed, and let me know if you have any suggestions for improving the content or the keywords.

```

---

<!-- rtbf_prompts_1.csv -->

## 8. VARIOUS PROMPT

**Un jeu de prompts remplissant des fonctions variées.**

### VARIOUS PROMPT #1
**Objectif:** 
Concevoir une formation

**Nom technique:** `designing_a_training_program`


```text
En tant que qu'expert en formation, conçoit une session de formation sur la cybersécurité pour tous les employés de l'entreprise. Détaillez les objectifs de formation, le contenu des modules, les méthodes de livraison et les critères d'évaluation, sous forme de tableau.
```

### VARIOUS PROMPT #2
**Objectif:** 
Créer un plan de communication (avec la technique de l'entonnoir)

**Nom technique:** `creating_communication_plan_with_funnel_technique`


```text
<!-- question_1 -->
En tant qu'expert en communication interne des organisations, rédige un plan de communication interne à la RTBF pour promouvoir une campagne de sensibilisation à la diversité et inclusion sous forme de tableau. Pose-moi des questions avant de répondre.


<!-- question_2 -->
Détaille la partie XXX du plan en indiquant les actions concrètes à mener, les livrables, des idées pour rendre cette étape du projet la plus créative et engageante possible et quelques conseils utiles pour la réussite de cette séquence de démarrage du projet.


<!-- question_3 -->
Rédige le script de la vidéo XXX de la partie XXX

<!-- question_4 -->
Rédige le mail qui sera envoyé aux collaborateurs lors du lancement de cette campagne pour les inviter à venir découvrir la vidéo d'introduction sur l'intranet de l'organisation. 

```


### VARIOUS PROMPT #3
**Objectif:** 
En tant que producteur de contenu vidéo

**Nom technique:** `video_content_producer_guidelines`


```text
Elaborez un synopsys pour un documentaire sur les innovations en énergie renouvelable. Incluez des segments d'interviews avec des experts et des visites de sites innovants, en précisant les principaux points de discussion et les visuels clés pour chaque scène.
```


### VARIOUS PROMPT #4
**Objectif:** 
Créer une stratégie réseaux sociaux

**Nom technique:** `create_social_media_strategy`

```text
En tant que spécialiste marketing, proposez une stratégie pour promouvoir notre nouvelle série de podcasts sur les réseaux sociaux. Détaillez les recommandations pour les plateformes cibles, les messages clés, et des idées pour des posts engageants qui attireraient l'audience cible.
```

### VARIOUS PROMPT #5
**Objectif:** 
Résumé une réunion

**Nom technique:** `meeting_summary`

```text
Agissez en tant qu'expert en formation. Résumez le compte-rendu de la réunion suivante sur un ton factuel pour en identifier les trois points clés, et présentez-les sous forme d'un tableau. Incluez les implications pour les prochaines étapes.
```

### VARIOUS PROMPT #6
**Objectif:** 
Rédiger un brief pour un designer

**Nom technique:** `design_brief_for_designer`

```text
En tant que chef de projet marketing, rédigez un brief pour un designer graphique pour la création d'une affiche promotionnelle pour notre prochain événement en ligne sur les médias numériques. Incluez le thème de l'événement, le public cible, les éléments visuels souhaités et les spécifications techniques.
```

### VARIOUS PROMPT #7
**Objectif:** 
Répondre à un mail

**Nom technique:** `reply_to_email`

```text
Agis en tant que responsable de XXX. Répond à ce mail sur un ton professionnel et chaleureux en indiquant que l'idée est intéressante et que tu souhaiterais en savoir plus. Demande également les disponibilités pour une visioconférence.
----
(copier ici le texte de l'email reçu)
```

---


<!-- 005_fmm_nlp_prompts_1.csv -->

**Un jeu de prompts plus avancés pour des fonctions de NLP (resumé, reconnaisance d'entités nommés...).**



## 9. PROMPT NLP


### PROMPT NLP #1
**Objectif:** 
Ce prompt est une demande pour résumer le texte d'entrée donné par l'utilisateur en un certain nombre de phrases spécifié.

La réponse doit contenir les idées principales et les points clés du texte, sans utiliser les mêmes phrases que dans le texte original.

Par exemple, si le texte d'entrée est "L'intelligence artificielle (IA) est un domaine de la recherche en informatique qui vise à créer des machines capables de simuler l'intelligence humaine. Les applications de l'IA sont nombreuses et variées, allant de la reconnaissance vocale aux jeux vidéo en passant par la conduite autonome. Cependant, l'IA soulève également des préoccupations éthiques et sociales, notamment en ce qui concerne la protection de la vie privée et le remplacement des emplois humains par des machines.", et que la longueur du résumé est de 2 phrases, la réponse doit être "L'intelligence artificielle est un domaine de recherche visant à créer des machines simulant l'intelligence humaine, avec de nombreuses applications. Cependant, des préoccupations éthiques et sociales sont soulevées, notamment concernant la protection de la vie privée et le remplacement d'emplois humains.".

**Nom technique:** `summary_length`

```text
Given the input text: Input: {source} Produce a {summary_length} sentences length summary of the text. Captures the main ideas and key points of the text. Summary Does not include verbatim sentences from the original text.
```

### PROMPT NLP #2
**Objectif:** 
Ce prompt est une demande pour extraire les motifs spécifiés dans le texte d'entrée donné par l'utilisateur.

La réponse doit contenir les valeurs correspondantes à chaque motif extrait, dans le format spécifié, c'est-à-dire "nom\_du\_motif:valeurs\_du\_motif...".

Par exemple, si le texte d'entrée est "Je suis né le 12/12/1990 à Paris. Mon numéro de téléphone est le 06 12 34 56 78", et que les motifs à extraire sont "date de naissance" et "numéro de téléphone", la réponse doit être "date de naissance:12/12/1990, numéro de téléphone:06 12 34 56 78".

**Nom technique:** `extract_patterns`


```text
Given the input text: user input: {source} extract following patterns from it: {patterns} output must be in this format:pattern_name: pattern_values...
```

### PROMPT NLP #3
**Objectif:** 
Ce prompt est une demande pour traduire le texte d'entrée donné par l'utilisateur dans la langue cible spécifiée.

La réponse doit contenir uniquement le texte traduit, sans aucune autre information.

Par exemple, si le texte d'entrée est "Bonjour, comment ça va ?" et que la langue cible est l'anglais, la réponse doit être "Hello, how are you ?".

**Nom technique:** `text_translate`


```text
Given the input text: user input: {source} convert it into {target_lang} language output must contain only the translated text
```

### PROMPT NLP #4
**Objectif:** 
Ce prompt est une demande pour remplacer des mots dans le texte original donné en entrée par l'utilisateur, en utilisant les règles de remplacement fournies.

La réponse doit contenir uniquement le texte modifié avec les remplacements effectués, sans aucune autre information.

Les mots doivent être remplacés même si la phrase ne fait plus de sens ou si le remplacement change le sens de la phrase.

La réponse doit être dans le format spécifié, c'est-à-dire "mot\_à\_remplacer:mot\_de\_remplacement".

Par exemple, si le texte d'entrée est "J'aime manger des pommes" et que la règle de remplacement est "pommes:bananes", la réponse doit être "J'aime manger des bananes".

**Nom technique:** `text_replace`


```text
Given the original text: user input: {source} And the replacement rule: replacement rule: {replacement_rules}__________________________Replace words in the original text according to the replacement rules provided. Apply the rules to modify the text. Only provide the output that has the modified text with replacements nothing else. Replace words even when sentence does not make sense. make sure all mentioned words must be replaced replace word even if change the meaning of the sentence or does not make sense output format: word_to_replace: replacement_word
```

### PROMPT NLP #5
**Objectif:** 
Ce prompt est une demande pour effectuer une reconnaissance d'entités nommées (NER) dans le texte donné en entrée par l'utilisateur.

La réponse doit contenir les entités nommées identifiées dans le texte, avec leur étiquette respective. Les étiquettes possibles sont : FAC, CARDINAL, NUMBER, DEMONYM, QUANTITY, TITLE, PHONE\_NUMBER, NATIONAL, JOB, PERSON, LOC, NORP, TIME, CITY, EMAIL, GPE, LANGUAGE, PRODUCT, ZIP\_CODE, ADDRESS, MONEY, ORDINAL, DATE, EVENT, CRIMINAL\_CHARGE, STATE\_OR\_PROVINCE, RELIGION, DURATION, URL, WORK\_OF\_ART, PERCENT, CAUSE\_OF\_DEATH, COUNTRY, ORG, LAW, NAME, COUNTRY, RELIGION, TIME.

La réponse doit être dans le format spécifié, c'est-à-dire "étiquette:valeur".

Par exemple, si le texte d'entrée est "Je vis à Paris, en France. Mon numéro de téléphone est le 06 12 34 56 78", la réponse doit être "LOC:Paris, COUNTRY:France, PHONE\_NUMBER:06 12 34 56 78".

**Nom technique:** `detect_ner`


```text
Given the input text:user input: {source} perform NER detection on it. NER TAGS: FAC;  CARDINAL;  NUMBER;  DEMONYM;  QUANTITY;  TITLE;  PHONE_NUMBER;  NATIONAL;  JOB;  PERSON;  LOC;  NORP;  TIME;  CITY;  EMAIL;  GPE;  LANGUAGE;  PRODUCT;  ZIP_CODE;  ADDRESS;  MONEY;  ORDINAL;  DATE;  EVENT;  CRIMINAL_CHARGE;  STATE_OR_PROVINCE;  RELIGION;  DURATION;  URL;  WORK_OF_ART;  PERCENT;  CAUSE_OF_DEATH;  COUNTRY;  ORG;  LAW;  NAME;  COUNTRY;  RELIGION;  TIME answer must be in the format tag:value
```


### PROMPT NLP #6
**Objectif:** 
Ce prompt est une demande pour résumer un texte donné en entrée, avec une longueur spécifique de phrases pour le résumé. Il demande à ce que le résumé capture les idées principales et les points clés du texte original, sans utiliser les mêmes phrases que dans le texte original. En d'autres termes, il faut reformuler les idées principales en respectant la longueur de résumé demandée.

**Nom technique:** `text_summarize`



```text
Given the input text: Input: {source} Produce a {summary_length} sentences length summary of the text. Captures the main ideas and key points of the text. Summary Does not include verbatim sentences from the original text.
```


### PROMPT NLP #7
**Objectif:** 
Ce prompt est une demande pour répondre à une question spécifique à partir d'un texte donné en entrée. Il demande à ce que la réponse soit pertinente et concise, sans fournir d'informations supplémentaires. Il est important que la réponse réponde directement à la question posée, en utilisant les informations contenues dans le texte original.

**Nom technique:** `text_qna`


```text
Given the input text: Input: {source} Answer the following question:  {question} The answer should be relevant and concise; without any additional information. Ensure that the answer directly addresses the question.
```


### PROMPT NLP #8
**Objectif:** 
Ce prompt est une demande pour identifier l'intention du texte donné en entrée par l'utilisateur. Si l'intention n'est pas claire, la réponse doit être "None". Si l'intention comporte plusieurs mots, ils doivent être séparés par des virgules. La réponse doit être dans le format spécifié, c'est-à-dire "Intent: intent1; intent2; ...".

De plus, le prompt demande de détecter si le texte est un spam ou non. Le nombre de classes de spam à détecter est spécifié dans la variable "num_classes". Il est important de ne fournir aucune autre information que celle demandée dans le format spécifié.

**Nom technique:** `text_intent`


```text
Given the input sentence: user input: {source} Identify the intent of the text. If no clear intent can be determined from the input; return None. If the output intent contains multiple words; separate them with comma. output must be in this format -> Intent: intent1; intent2; ...
```


### PROMPT NLP #9
**Objectif:** 
Ce prompt demande à l'utilisateur d'effectuer une détection de spam sur un texte d'entrée donné. Le prompt spécifie également le nombre de classes de spam à détecter, à l'aide de la variable `{num_classes}`. L'utilisateur ne doit fournir aucune autre information que le format de réponse spécifié par la variable `{format_answer}`.

**Nom technique:** `detect_spam`


```text
# version_1
Given the input text; perform spam detection on it  {source} num_classes: {num_classes} You must not provide any other information than the format {format_answer}
```

```text
# version_2
Instruction: Classify the following text as spam or not spam.

Background: The text is from an email sent to a large number of recipients. The email contains a promotional offer for a product. The purpose of the spam detection is to filter out unwanted and potentially harmful emails.

Expectations:

* Use 1 for spam and 0 for not spam.
* Provide a probability score between 0 and 1, like this: "0.9"
* Do not provide any other information than the format: "{format_answer}"

Output: {format_answer}

Text: {source}

Note: Feel free to ask for clarification if needed, and let me know if you have any suggestions for improving the text or the spam detection.
```

### PROMPT NLP #10
**Objectif:** 
Ce prompt est une demande pour corriger les fautes d'orthographe dans le texte donné en entrée par l'utilisateur. La réponse doit être dans le format spécifié, c'est-à-dire "misspelled\_word:corrected\_word ...", où les mots mal orthographiés sont suivis de deux points et des mots correctement orthographiés. Il est important de ne fournir aucune autre information que celle demandée dans le format spécifié.

**Nom technique:** `text_spellcheck`


```text
Given the input text: user input: {source} output must be in this format: misspelled_word:corrected_word ... output must not contain any other information than the format
```

### PROMPT NLP #11
**Objectif:** 
Ce prompt est une demande pour effectuer une analyse sémantique de la phrase donnée en entrée par l'utilisateur, en utilisant l'étiquetage de rôles sémantiques (SRL). L'objectif est d'identifier le prédicat, l'agent et le thème de la phrase.

Le prédicat est l'action ou l'état décrit par le verbe. L'agent est l'entité qui effectue l'action. Le thème est l'entité qui est affectée par l'action.

La réponse doit être dans le format spécifié, c'est-à-dire :

* Prédicat : [prédicat]
* Agent : [agent]
* Thème : [thème]

Si un composant n'est pas présent ou ne peut pas être identifié, la réponse doit être "None" pour ce composant.

**Nom technique:** `text_srl`


```text
Given the input sentence: user input: {source} __________________________ Perform Semantic Role Labeling (SRL) on the input sentence to identify the predicate; agent; and theme. - Predicate: The action or state described by the verb. - Agent: The entity performing the action. - Theme: The entity that is affected by the action. Ensure the output follows this format: - Predicate: [predicate] - Agent: [agent] - Theme: [theme] If any component is not present or cannot be identified; return None for that component.
```


### PROMPT NLP #12
**Objectif:** 
Ce prompt est une demande pour effectuer une analyse grammaticale de la phrase donnée en entrée par l'utilisateur, en utilisant l'étiquetage de parties du discours (POS).

L'objectif est d'identifier les différentes parties du discours dans la phrase, telles que les noms, les verbes, les adjectifs, les adverbes, les pronoms, les prépositions, les conjonctions, les interjections, les déterminants, les nombres, les dates, les heures, etc.

La réponse doit être dans le format spécifié, c'est-à-dire "tag:value", où "tag" est l'étiquette de la partie du discours et "value" est le mot correspondant. Par exemple, "noun:chat" pour le mot "chat" étiqueté comme un nom.

**Nom technique:** `detect_pos`



```text
Given the input text: user input: {source} perform POS detection on it. POS TAGS:noun;  verb;  adjective;  adverb;  pronoun;  preposition;  conjunction;  interjection;  determiner;  cardinal;  foreign;  number;  date;  time;  ordinal;  money;  percent;  symbol;  punctuation;  emoticon;  hashtag;  email;  url;  mention;  phone;  ip;  cashtag;  entity;  answer must be in the format tag:value
```


### PROMPT NLP #13
**Objectif:** 

Ce prompt est une demande pour identifier les émojis dans le texte donné en entrée par l'utilisateur et les remplacer par leur représentation textuelle.

La réponse doit être le texte mis à jour avec les émojis remplacés par leur représentation textuelle. Il est important de ne fournir aucune autre information que celle demandée dans la réponse.

Par exemple, si le texte d'entrée est "J'adore les chats 🐱", la réponse doit être "J'adore les chats (chat)".

**Nom technique:** `text_emojis`



```text
Given the input text: user input: {source} Identify the emojis in the text and replace them with their text representation. output must be the updated text with emojis replaced by their text representation. output must not contain any other information than the updated text.
```


### PROMPT NLP #14
**Objectif:** Ce prompt est une demande pour identifier et extraire les expressions idiomatiques présentes dans la phrase donnée en entrée par l'utilisateur.

La réponse doit contenir uniquement les expressions idiomatiques extraites. Il est important de ne pas inclure de puces ou d'autres informations dans la réponse.

Si plusieurs expressions idiomatiques sont trouvées, elles doivent être retournées dans de nouvelles lignes. Si aucune expression idiomatique n'est trouvée, la réponse doit être "None".

Par exemple, si la phrase d'entrée est "Il pleut des cordes", la réponse doit être "pleut des cordes".

**Nom technique:** `text_idioms`



```text
Given the input sentence: user input: {source} __________________________ Identify and extract any idioms present in the sentence. Output must only contain the extracted idioms. Output must not contain any bullet points. If there is more than one idiom found; return both in new lines. If no idiom is found; return None. output must be in this format: extracted idioms ... output must not contain any other information than the extracted idioms.
```

### PROMPT NLP #15
**Objectif:** Ce prompt est une demande pour détecter les anomalies ou les valeurs aberrantes dans le texte donné en entrée par l'utilisateur.

La réponse doit contenir uniquement les anomalies ou les valeurs aberrantes détectées. Il est important de ne pas inclure d'autres informations, de puces ou de tout autre formatage dans la réponse.

La réponse doit être dans le format spécifié, c'est-à-dire "anomalies détectées ...".

Par exemple, si le texte d'entrée est "Je suis né en 1992 et j'ai 300 ans", la réponse doit être "300 ans".


**Nom technique:** `text_anomaly`



```text
Given the input sentence: user input: {source} Detect any anomalies or outliers in the text. output only the detected anomalies and do not provide any other information do not use bullet points or any other formatting output must be in this format: detected anomalies ... output must not contain any other information than the detected anomalies.
```

### PROMPT NLP #16
**Objectif:** 

Ce prompt est une demande pour effectuer une résolution de coréférences dans le paragraphe donné en entrée par l'utilisateur, afin d'identifier ce que chaque pronom dans le paragraphe représente.

La réponse doit contenir uniquement les références résolues pour chaque pronom, sans aucun contexte supplémentaire. Il est important de ne pas inclure de puces ou d'autres informations dans la réponse.

Si aucune référence n'est trouvée pour un pronom, la réponse doit être "None".

La réponse doit être dans le format spécifié, c'est-à-dire "Pronom : Référent ...".

Par exemple, si le paragraphe d'entrée est "Marie a acheté une voiture. Elle est rouge et elle a l'air rapide", la réponse doit être "Elle : Marie, elle : voiture".


**Nom technique:** 
`text_coreference`



```text
Given the input paragraph: user input: {source} __________________________ Perform coreference resolution to identify what each pronoun in the paragraph is referring to. Output must only contain the resolved references for each pronoun; without any additional context. Output must not contain any bullet points. If no referent is found for a pronoun; return 'None'. Output must be in this format: Pronoun: Referent ... output must not contain another information.
```

<!-- 
Expliquer en francais ce que fait ce prompt: 

```text
Conçoit une session de formation sur la cybersécurité pour tous les employés de l'entreprise. Détaillez les objectifs de formation, le contenu des modules, les méthodes de livraison et les critères d'évaluation, sous forme de tableau.
```

Create a filename in english from this sentence below with no accent and instead of space a "_"  

```text
Créer une stratégie réseaux sociaux
```

-->