
# 001_ia_kpi_llm.md



## DRAFT_PROMPT_1


En tant que consultant RSE, architecte API et développeur python, peux tu répondre à ces questions avec ce double objectif :

# objectifs
- Il est de savoir s'il existe des outils ou si l'on peut construire des outils ou des scripts en python pour mesurer et monitorer l'empreinte carbone du fonctionnement d'une API.
- Il est nécessaire d'avoir une matrice décisionnelle pour arbitrer le développement d'une API et des LLM qui la structurent en fonction de l'impact carbone. En effet, le direction de projet pourrait renoncer à une activation partielle voir complète de certains microservices ou de réduire le volume de fichiers si l'arbitrage sur le bilan carbone se révèle défavorable.

# précisions
1. Le périmètre fonctionnel de l'api et les technologies utilisées:
Cette API est une API faite avec Fastapi. Fonctionnellement, cette API  délivre plusieurs micro service d'intelligence  artificielle : comme par exemple un endpoint de transcription avec whisper, un endpoint de traduction avec NLLB, un endpoint d'IAG avec la version 7B du modèle Mistral distribué à l'aide de ollama...
La liste des endpoints n'est pas exhaustive et va s'accroître dans le temps.

En effet, en fonction de la cartographie des cas d'usage recensé, le périmètre des endpoints peut augmenter.


2. Le volume de fichiers
Pour ce qui est du volume de fichiers, qui rentre en ligne de compte dans le calcul, on peut estimer que le volume de fichiers va être exponentiel, on peut partir sur une estimation au mois de le mois de 500 fichiers, puis faire croître cette suite de fichiers de 500 par mois.

Il faudra déterminer un nombre de fichiers moyens et de la changer de manière exponentielle au cours du temps.

Le volume de fichiers va augmenter mécaniquement parce l'API va activer les mêmes microservices mais dans des langues différentes. Pour les langues, on va commencer dans l'ordre par le francais (FR), l'anglais (EN), l'espagnol (ES) puis l'arabe (AR). 

Cette activation progressive des langues dans le temps est un point important dont il faut tenir compte dans le raisonnement car il faut distinguer que le nombre de fichiers audio, vidéo, texte peut varier par langue par ex Le volume en ES peut-être inférieur au volume. Dans le raisonnement comme dans les scripts éventuels met en évidence les scripts éventuels cette activation progressive des langues.




2. La typologie du contenu (fichiers audio vidéo et texte)

Il s’agit de fichiers audio et vidéo pour la transcription mais aussi de fichiers textes pour l'IAG. sans connaître la durée moyenne, il faudra donc déterminer la durée moyenne d'un audio et d'une vidéo pour lors de l'opération transcription connaître l'impact carbone de cette opération.
Idem pour le texte, on parle d'articles qui font entre 3000 et 5000 signes donc qu'il faudra convertir en tokens.

Il faudra déterminer une durée moyenne pour un fichier audio, un fichier vidéo, un fichier texte moyen. La durée ou la taille de ses fichier audio, vidéo et texte va peut varier dans le temps


3. Le service d'hébergement

Cette API sera hébergé sur le Cloud azure


# output
Premièrement, peux-tu établir un diagnostic sur le raisonnement compte tenu des propositions faites sur les points 1, 2 et 3

Deuxièmement, peux-tu donner des infos sur la stratégie à adopter pour parvenir à cet objectif soit du build soit du buy avec des outils payants gratuits, des packages python existants... etc


Troisièmement, faire une liste détaillée des actions à mener si on décide de passer en build et de commencer à coder en python les scripts correspond jouant avec 



# note
Tout le code doit être commenté n’hésite pas à recourir aux bonnes pratiques de programmation  en utilisant des classes de fonctions afin de rendre le code lisible et maintenable.




## PROMPT_1

En tant qu'expert en prompt, peux-tu corriger et améliorer ce prompt en francais ci-dessous afin de faire en sorte qu'il soit le plus efficient possible sur un LLM.

```text
En tant que consultant RSE, architecte API et développeur python, peux tu répondre à ces questions avec ce double objectif :

# objectifs
- Il est de savoir s'il existe des outils ou si l'on peut construire des outils ou des scripts en python pour mesurer et monitorer l'empreinte carbone du fonctionnement d'une API.
- Il est nécessaire d'avoir une matrice décisionnelle pour arbitrer le développement d'une API et des LLM qui la structurent en fonction de l'impact carbone. En effet, le direction de projet pourrait renoncer à une activation partielle voir complète de certains microservices ou de réduire le volume de fichiers si l'arbitrage sur le bilan carbone se révèle défavorable.

# précisions
1. Le périmètre fonctionnel de l'api et les technologies utilisées:
Cette API est une API faite avec Fastapi. Fonctionnellement, cette API  délivre plusieurs micro service d'intelligence  artificielle : comme par exemple un endpoint de transcription avec whisper, un endpoint de traduction avec NLLB, un endpoint d'IAG avec la version 7B du modèle Mistral distribué à l'aide de ollama...
La liste des endpoints n'est pas exhaustive et va s'accroître dans le temps.

En effet, en fonction de la cartographie des cas d'usage recensé, le périmètre des endpoints peut augmenter.


2. Le volume de fichiers
Pour ce qui est du volume de fichiers, qui rentre en ligne de compte dans le calcul, on peut estimer que le volume de fichiers va être exponentiel, on peut partir sur une estimation au mois de le mois de 500 fichiers, puis faire croître cette suite de fichiers de 500 par mois.

Il faudra déterminer un nombre de fichiers moyens et de la changer de manière exponentielle au cours du temps.

Le volume de fichiers va augmenter mécaniquement parce l'API va activer les mêmes microservices mais dans des langues différentes. Pour les langues, on va commencer dans l'ordre par le francais (FR), l'anglais (EN), l'espagnol (ES) puis l'arabe (AR). 

Cette activation progressive des langues dans le temps est un point important dont il faut tenir compte dans le raisonnement car il faut distinguer que le nombre de fichiers audio, vidéo, texte peut varier par langue par ex Le volume en ES peut-être inférieur au volume. Dans le raisonnement comme dans les scripts éventuels met en évidence les scripts éventuels cette activation progressive des langues.




2. La typologie du contenu (fichiers audio vidéo et texte)

Il s’agit de fichiers audio et vidéo pour la transcription mais aussi de fichiers textes pour l'IAG. sans connaître la durée moyenne, il faudra donc déterminer la durée moyenne d'un audio et d'une vidéo pour lors de l'opération transcription connaître l'impact carbone de cette opération.
Idem pour le texte, on parle d'articles qui font entre 3000 et 5000 signes donc qu'il faudra convertir en tokens.

Il faudra déterminer une durée moyenne pour un fichier audio, un fichier vidéo, un fichier texte moyen. La durée ou la taille de ses fichier audio, vidéo et texte va peut varier dans le temps


3. Le service d'hébergement

Cette API sera hébergé sur le Cloud azure


# output
Premièrement, peux-tu établir un diagnostic sur le raisonnement compte tenu des propositions faites sur les points 1, 2 et 3

Deuxièmement, peux-tu donner des infos sur la stratégie à adopter pour parvenir à cet objectif soit du build soit du buy avec des outils payants gratuits, des packages python existants... etc


Troisièmement, faire une liste détaillée des actions à mener si on décide de passer en build et de commencer à coder en python les scripts correspond jouant avec 



# note
Tout le code doit être commenté n’hésite pas à recourir aux bonnes pratiques de programmation  en utilisant des classes de fonctions afin de rendre le code lisible et maintenable.



```

## MISTRAL_1

Bien sûr, voici le texte brut sans les tags de readme :

```text
En tant que consultant RSE, architecte API et développeur Python, peux-tu répondre aux questions suivantes avec un double objectif :

Objectifs
1. Mesure et Monitoring de l'Empreinte Carbone :
   - Identifier s'il existe des outils ou si l'on peut développer des scripts en Python pour mesurer et monitorer l'empreinte carbone du fonctionnement d'une API.

2. Matrice Décisionnelle :
   - Élaborer une matrice décisionnelle pour arbitrer le développement d'une API et des LLM qui la structurent en fonction de l'impact carbone. Cela permettra à la direction de projet de renoncer à l'activation partielle ou complète de certains microservices ou de réduire le volume de fichiers si l'arbitrage sur le bilan carbone se révèle défavorable.

Précisions

1. Périmètre Fonctionnel de l'API et Technologies Utilisées :
   - L'API est développée avec FastAPI et offre plusieurs microservices d'intelligence artificielle, tels qu'un endpoint de transcription avec Whisper, un endpoint de traduction avec NLLB, et un endpoint d'IAG avec la version 7B du modèle Mistral distribué via Ollama.
   - La liste des endpoints n'est pas exhaustive et pourra s'accroître en fonction des cas d'usage recensés.

2. Volume de Fichiers :
   - Le volume de fichiers est estimé à 500 fichiers par mois, avec une croissance exponentielle.
   - L'API activera les mêmes microservices dans différentes langues : français (FR), anglais (EN), espagnol (ES), puis arabe (AR).
   - Le nombre de fichiers audio, vidéo et texte peut varier par langue. Par exemple, le volume en espagnol peut être inférieur à celui en français.

3. Typologie du Contenu :
   - Les fichiers incluent des audio et vidéo pour la transcription, ainsi que des fichiers texte pour l'IAG.
   - La durée moyenne des fichiers audio et vidéo doit être déterminée pour évaluer l'impact carbone de l'opération de transcription.
   - Les articles textuels font entre 3000 et 5000 signes, à convertir en tokens.

4. Service d'Hébergement :
   - L'API sera hébergée sur le Cloud Azure.

Output

1. Diagnostic :
   - Établir un diagnostic sur le raisonnement compte tenu des propositions faites sur les points 1, 2 et 3.

2. Stratégie :
   - Donner des informations sur la stratégie à adopter pour parvenir à cet objectif, que ce soit en optant pour des solutions existantes (buy) ou en développant des outils (build). Inclure des outils payants, gratuits, et des packages Python existants.

3. Actions à Mener :
   - Faire une liste détaillée des actions à mener si l'on décide de passer en mode build et de commencer à coder les scripts correspondants en Python.

Note
- Tout le code doit être commenté.
- Recourir aux bonnes pratiques de programmation en utilisant des classes et des fonctions pour rendre le code lisible et maintenable.
```

Vous pouvez maintenant copier ce texte et le coller dans un éditeur de texte pour l'enregistrer en tant que fichier .txt.



## SOURCE

KPI de mesure : Perf temps de processus, nombre de tokens pricing comparatif des prix avec model payants, RSE empreinte carbone

TODO : Trouver comment mesurer l'empreinte carbone
TOOLS : outils de mesure, suivi de la bécane, suivi du LLM...






## DEPOT
1. Maintenir un ton professionnel mais {TONE}
2. Préserver la force des arguments et des critiques tout en évitant le langage familier
3. Reformuler les expressions familières en équivalents soutenus sans édulcorer le message
4. Conserver la structure argumentative et les analyses critiques
5. Garder les métaphores et analogies pertinentes en les reformulant de manière plus formelle
6. Supprimer les marques de subjectivité excessive tout en maintenant la fermeté du propos

L'objectif est de rendre le message présentable professionnellement sans en diluer la substance critique et analytique.







