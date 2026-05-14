

Peux-tu écrire un fichier claude.md pour ce projet, en organisant les éléments et en les amendant au besoin. Le développement de pipeline et du plugin sera ensuite fait à l'aide de claude code.

## OBJECTIF : 

1. Via une pipeline en python, classer les tags des posts issues d'un WordPress (taxonomy=post_tag, taxonomy=category) automatiquement afin de construire un fil d'ariane et validé son enrichissement Wikidata et Spacy (entités nommés). La finalité de la pipeline est de manipuler ensuite via un pugin dans le backoffice de WP ces tags des posts (taxonomy=post_tag, taxonomy=category) afin d'afficher ensuite un fil d'ariane optimisé.


3. Il faut pouvoir dans le plugin simuler le fil d'ariane, la traduction,, l'enrichissement, le slug  avant de valider le changement en production d'un tag issu du taxonomy=post_tag et taxonomy=category parce que c’est une création automatique qui peut être validé editorialement.

- Comme le fil d'ariane est une création ad hoc je peux stocker ces changement dans une table mysql additionnelle liés au plugin, ne pas hésiter à préserver les éléments originaux. Ce plugin doit etre disponible sur une destination unique du type /wp-admin/admin.php?page=breadcrumb-migration

- UX possible du plugin : Mapping element originaux (colonne de gauche) et éléments modifiés   (colonne de droite) avec tous les éléments pour opérer le changement optimisé afin de produire  le fil d'ariane, la traduction,, l'enrichissement, le slug  avant de valider le changement en production d'un tag issu du taxonomy=post_tag et taxonomy=category


3. Il existe un docker complet du wordpress avec l'ensemble de la base du wordpress afin  d'avoir un environnment de staging.


```bash
# command coming soon

```
## RÉGLES

### 1. GROUPE PRIMAIRE
Tag catégorie
Les tags issus de taxonomy=category

- Sous-Rubrique
ex: Home › AI 

- IMPACT SUR URL ET BREADCRUMB
URL : Voir si je renomme les url via le label et le slug, il faudrait que je puisse faire une table de redirection.

```text
URL: https://flaven.fr/category/ux-experience-utilisateur/ (KO)
URL: https://flaven.fr/category/ux-user-experience/ (OK)
Breadcrumb: Home › UX
```


Fil d'Ariane : création du fil d'ariane le plus pertinent
Tout est fait pour générer un fil d'ariane cohérent Cf. articulation taxonomy=category et taxonomy=post_tag
 

### 2. GROUPE SECONDAIRE
Tag thématiques
Les tags issus de taxonomy=post_tag

- Le tag thématique est attaché editorialement à une categorie
ex: Home › AI › Claude Code
Note: le tag thématique est attaché à un tag de section. 


## PLUGIN WORPRESS
Il faut pouvoir via le plugin en cas de création de tags dans taxonomy=post_tag, taxonomy=category mener via le plugin plusieurs operations manuellemny afin de pouvoir enrichir la tag :
- affecter un wikidata_id
- affecter une des 18 entités nommés de Spacy
- simuler la fil d'ariane avant validation et publication? Les fil d'ariane doit être cliquable 


Il faut que je puisse changer, créer des categories au besoin pour avoir le meilleur fil d'ariane possible et le classemnt SEO optimal.

Home › Agile › Claude Code (KO)
Home › AI › Claude Code (OK)


- ajouter un texte de description soit écrit manuellement soit émanant de wikidata, une fois que l'identification du tag est sans équivoque,  sur la page frontend category pour améliorer la performance de référencement naturel
- ajouter un texte de description sur la page frontend category pour améliorer la performance de référencement naturel

```text
--- taxonomy=category)
URL: https://flaven.fr/category/agile/ 
Breadcrumb: Home › Agile
URL: https://flaven.fr/category/ux-experience-utilisateur/ 
Breadcrumb: Home › UX
URL: https://flaven.fr/category/tutoriaux/  
Breadcrumb: Home › Tutoriaux
etc...
--- taxonomy=post_tag
URL: https://flaven.fr/tag/ai/
Breadcrumb: Home › Développement › AI
URL: https://flaven.fr/tag/wordpress/
Breadcrumb: Home › Wordpress
URL: https://flaven.fr/tag/python/
Breadcrumb: Home › Technologie › python
URL: https://flaven.fr/tag/php/
Breadcrumb: Home › Wordpress › PHP
etc...
```


## WORKFLOW STEP BY STEP

+ STEP_1 : 
Lister les taxonomies Categories et Tags (taxonomy=category et taxonomy=post_tag) des posts (post) en français et avoir la possibilité de les traduire en anglais. Indiquer l'id et le nombre de contenu attaché à chaque tag catégorie.

+ STEP_2 : 
Extraire avec l'aide de Spacy les entités nommés de ces taxonomies Categories et Tags


+ STEP_3 : 
Faire un recherche sur Wikidata à partir du label du tag afin eventulementy de l'enrichir.

A compléter.... avec les autres étapes necessaire au WORKFLOW 


## MUST-HAVE

1. Sans doute faire un backup des table originales des tags et des catégories du WP avant de faire des changements et que le traitement puisse se faire dans des tables séparées pour éviter pour le moment de modifier les tables originales.
 
2. Voici la liste des entités nommés qui pourrait être selctionne via un menu déroulant, donner un exmmle pour chque type d'entité e.g PERSON Nelson Mandela
--- name entities from Spacy
PERSON:      People, including fictional.
NORP:        Nationalities or religious or political groups.
FAC:         Buildings, airports, highways, bridges, etc.
ORG:         Companies, agencies, institutions, etc.
GPE:         Countries, cities, states.
LOC:         Non-GPE locations, mountain ranges, bodies of water.
PRODUCT:     Objects, vehicles, foods, etc. (Not services.)
EVENT:       Named hurricanes, battles, wars, sports events, etc.
WORK_OF_ART: Titles of books, songs, etc.
LAW:         Named documents made into laws.
LANGUAGE:    Any named language.
DATE:        Absolute or relative dates or periods.
TIME:        Times smaller than a day.
PERCENT:     Percentage, including ”%“.
MONEY:       Monetary values, including unit.
QUANTITY:    Measurements, as of weight or distance.
ORDINAL:     “first”, “second”, etc.
CARDINAL:    Numerals that do not fall under another type.



