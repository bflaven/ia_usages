Oui — je te propose ci-dessous un **claude.md** structuré et amendé pour cadrer le travail de **Claude Code** sur ce projet. Il transforme ton besoin en cahier des charges opérationnel, avec objectifs, architecture, workflow, règles métiers, modèle de données et backlog technique. Les éléments sont organisés pour permettre une implémentation progressive d’abord de la pipeline Python, puis du plugin WordPress d’édition/validation. Les principes retenus s’appuient sur spaCy pour la NER, sur l’API de recherche Wikidata pour l’enrichissement, et sur une page d’admin WordPress dédiée via `add_menu_page()` pour le backoffice. [spacy](https://spacy.io/usage/linguistic-features)

## claude.md

```md
# Projet : Breadcrumb Migration WordPress

## Contexte

Ce projet vise à construire une chaîne de traitement en deux parties :

1. Une **pipeline Python** qui analyse les taxonomies WordPress `category` et `post_tag`, les classe, les enrichit, et propose une structure de fil d’ariane cohérente.
2. Un **plugin WordPress** dédié au backoffice qui permet de simuler, valider, modifier et publier les changements de taxonomies et de breadcrumbs de façon éditoriale.

Le besoin principal est de produire des breadcrumbs SEO pertinents à partir de taxonomies existantes, sans modifier immédiatement les données originales. Les changements doivent pouvoir être simulés, validés, historisés, puis appliqués en production.

---

## Objectifs fonctionnels

### 1. Pipeline Python
La pipeline doit :

- Lister les termes des taxonomies `category` et `post_tag`.
- Identifier les termes en français et proposer une traduction en anglais.
- Extraire les entités nommées avec spaCy.
- Chercher un enrichissement Wikidata pour chaque terme.
- Proposer une classification métier des termes :
  - groupe primaire : catégories / sous-rubriques.
  - groupe secondaire : tags thématiques rattachés à une catégorie.
- Générer une proposition de breadcrumb.
- Préparer les données pour le plugin WordPress.
- Conserver un historique complet des propositions et des validations.

### 2. Plugin WordPress
Le plugin doit permettre :

- de visualiser les taxonomies sous forme de mapping :
  - colonne gauche : élément original,
  - colonne droite : élément enrichi / modifié / validé.
- de simuler le breadcrumb avant validation.
- de modifier le label, le slug, la description, la traduction, l’entité spaCy, le wikidata_id.
- de créer de nouvelles catégories si nécessaire pour améliorer la cohérence du fil d’ariane.
- de valider ou rejeter une proposition avant publication.
- de stocker les modifications dans des tables séparées, sans écraser les données originales.
- de gérer les redirections si le slug ou le label change.

### 3. Environnement
Un environnement Docker WordPress complet existe déjà avec la base de données, et doit servir d’environnement de staging pour les tests et validations.

---

## Règles métier

### Groupe primaire : catégories
Les termes de `taxonomy=category` représentent des rubriques ou sous-rubriques structurantes.

Exemples :
- `Home › AI`
- `Home › UX`
- `Home › Tutoriaux`

Ces catégories peuvent être renommées si cela améliore :
- la lisibilité SEO,
- la cohérence éditoriale,
- la clarté du breadcrumb,
- la qualité du slug.

Exemple de transformation :
- `ux-experience-utilisateur` → `ux-user-experience`

Le système doit préserver la compatibilité via une table de redirection.

### Groupe secondaire : tags thématiques
Les termes de `taxonomy=post_tag` représentent des thèmes rattachés éditorialement à une catégorie.

Exemples :
- `Home › AI › Claude Code`
- `Home › WordPress › PHP`
- `Home › Technologie › Python`

Ces tags peuvent :
- être enrichis,
- être rattachés à une catégorie cible,
- être renommés,
- recevoir une traduction,
- être associés à une entité spaCy,
- être liés à un item Wikidata.

---

## Exigences éditoriales

Le breadcrumb doit être :
- pertinent,
- cliquable,
- cohérent avec l’arborescence éditoriale,
- optimisé pour le SEO,
- compatible avec les URL publiques.

Le système doit permettre d’ajouter :
- une description manuelle,
- ou une description issue de Wikidata quand l’identification est sans équivoque.

La description peut être affichée sur la page frontend de catégorie pour renforcer le référencement naturel.

---

## Workflow cible

### STEP 1 — Inventaire
Lister les termes de `category` et `post_tag` :
- id,
- nom,
- slug,
- langue,
- nombre de contenus associés,
- hiérarchie parent/enfant,
- URL actuelle.

Produire aussi une version traduisible en anglais.

### STEP 2 — Analyse NLP
Utiliser spaCy pour extraire les entités nommées et proposer un type d’entité parmi les labels disponibles.

### STEP 3 — Recherche Wikidata
Chercher un identifiant Wikidata à partir du label du terme.
Conserver :
- wikidata_id,
- label,
- description,
- alias,
- langue.

### STEP 4 — Classification métier
Déterminer si le terme est :
- une catégorie structurante,
- un tag thématique,
- un terme ambigu,
- un terme à valider manuellement.

### STEP 5 — Proposition de breadcrumb
Générer une arborescence candidate :
- Home › ...
- navigation cliquable,
- hiérarchie optimisée.

### STEP 6 — Simulation éditoriale
Permettre dans le plugin :
- prévisualisation du breadcrumb,
- prévisualisation du slug,
- prévisualisation du label,
- prévisualisation de la traduction,
- prévisualisation de la description,
- prévisualisation de l’impact URL.

### STEP 7 — Validation
Après validation humaine :
- enregistrer l’état validé,
- conserver les anciennes valeurs,
- déclencher les redirections si nécessaire,
- publier les mises à jour.

### STEP 8 — Synchronisation
Exporter les modifications validées vers WordPress :
- taxonomy `category`,
- taxonomy `post_tag`,
- tables annexes de mapping,
- table de redirection.

---

## Modèle de données

Ne jamais modifier immédiatement les données d’origine.
Préférer un stockage séparé dans des tables additionnelles.

### Tables suggérées

#### `wp_breadcrumb_migration_terms`
Stocke la copie fonctionnelle des termes analysés.
- original_term_id
- taxonomy
- original_name
- original_slug
- original_description
- original_parent_id
- language
- content_count
- current_status

#### `wp_breadcrumb_migration_proposals`
Stocke les propositions de transformation.
- proposal_id
- original_term_id
- proposed_name
- proposed_slug
- proposed_description
- proposed_language
- proposed_parent_id
- proposed_breadcrumb
- proposed_type
- proposed_spacy_entity
- proposed_wikidata_id
- validation_state
- created_at
- updated_at

#### `wp_breadcrumb_migration_redirects`
Gère les redirections d’URL.
- original_url
- new_url
- taxonomy
- term_id
- redirect_status
- active

#### `wp_breadcrumb_migration_audit`
Journalise les actions.
- user_id
- action_type
- entity_type
- entity_id
- old_value
- new_value
- timestamp

---

## Plugin WordPress

### Page admin unique
Le plugin doit être accessible via une destination unique :

`/wp-admin/admin.php?page=breadcrumb-migration`

### UX attendue
La page admin doit afficher :
- un tableau de mapping,
- la colonne gauche pour l’original,
- la colonne droite pour la version proposée,
- un état de validation,
- un bouton de simulation,
- un bouton d’édition,
- un bouton de validation,
- un bouton de rejet,
- un bouton de publication.

### Fonctions attendues
Le plugin doit permettre :
- de créer / éditer des catégories,
- de renommer des catégories et tags,
- de changer les slugs,
- d’assigner un `wikidata_id`,
- d’assigner un label spaCy,
- d’ajouter une description,
- de simuler le breadcrumb,
- de prévisualiser l’URL finale,
- de valider les changements.

### Redirections
Si le slug change :
- créer une redirection 301,
- conserver l’ancien chemin,
- vérifier l’absence de conflit avec d’autres taxonomies.

---

## Intégration breadcrumbs

Le fil d’ariane doit pouvoir être calculé à partir :
- de la hiérarchie WordPress native,
- de la taxonomie catégorie,
- du rattachement thématique des tags,
- des règles éditoriales.

Le breadcrumb doit être :
- déterministe,
- cliquable,
- lisible,
- réutilisable dans le thème ou via shortcode.

---

## Spécifications spaCy

Le projet doit supporter les entités nommées suivantes :

- PERSON : personnes.
- NORP : nationalités, groupes religieux ou politiques.
- FAC : bâtiments, aéroports, routes, ponts.
- ORG : entreprises, agences, institutions.
- GPE : pays, villes, États.
- LOC : lieux non géopolitiques.
- PRODUCT : objets, véhicules, aliments.
- EVENT : événements nommés.
- WORK_OF_ART : œuvres.
- LAW : documents juridiques.
- LANGUAGE : langues.
- DATE : dates.
- TIME : heures.
- PERCENT : pourcentages.
- MONEY : montants.
- QUANTITY : quantités.
- ORDINAL : ordinaux.
- CARDINAL : nombres.

Le menu déroulant du plugin doit permettre de sélectionner un type d’entité parmi ces labels.

---

## Recherche Wikidata

La recherche Wikidata doit :
- partir du label du terme,
- récupérer les candidats possibles,
- permettre une validation manuelle si plusieurs résultats existent,
- stocker le meilleur candidat,
- conserver les alternatives si nécessaire.

Le système doit gérer les cas ambigus :
- homonymies,
- termes génériques,
- labels multilingues,
- absence de correspondance claire.

---

## SEO et contenu
Si un terme est validé comme concept stable, le plugin peut :
- injecter une description sur la page catégorie,
- améliorer le maillage interne,
- enrichir les données structurées,
- faciliter le référencement naturel.

Le texte de description peut être :
- rédigé manuellement,
- importé depuis Wikidata,
- ou généré à partir d’une synthèse validée.

---

## Contraintes techniques

- Ne jamais écraser les tables d’origine sans validation explicite.
- Préférer des tables custom pour les propositions et le workflow.
- Prévoir un mode staging dans Docker.
- Prévoir un mode de simulation avant publication.
- Prévoir des logs d’audit.
- Prévoir un mécanisme de rollback.
- Prévoir des tests sur l’impact URL et breadcrumb.
- Prévoir une architecture compatible avec un développement assisté par Claude Code.

---

## Livrables attendus

1. Pipeline Python d’inventaire et d’enrichissement.
2. Schéma SQL des tables additionnelles.
3. Plugin WordPress avec page admin dédiée.
4. Moteur de simulation de breadcrumb.
5. Système de validation éditoriale.
6. Gestion des slugs et redirections.
7. Export/import entre pipeline et WordPress.
8. Documentation d’usage.

---

## Priorités d’implémentation

### Phase 1
- inventaire des taxonomies,
- stockage dans tables séparées,
- interface admin minimale,
- simulation breadcrumb.

### Phase 2
- intégration spaCy,
- recherche Wikidata,
- mapping éditorial.

### Phase 3
- validation éditoriale,
- redirections,
- descriptions SEO,
- publication contrôlée.

### Phase 4
- automatisation avancée,
- amélioration UX,
- tests d’intégration,
- robustesse multi-langue.

---

## Critères d’acceptation

Le projet est valide si :
- les taxonomies sont listées correctement,
- les propositions sont simulables,
- les données originales sont préservées,
- les changements sont validables manuellement,
- les breadcrumbs générés sont cohérents,
- les URLs restent maîtrisées,
- les redirections fonctionnent,
- les enrichissements spaCy / Wikidata sont stockés,
- l’admin page est accessible dans WordPress,
- le tout est exploitable ensuite avec Claude Code.
```

## Ajustements recommandés
J’ai volontairement corrigé et clarifié plusieurs points : la hiérarchie entre `category` et `post_tag`, la séparation entre **proposition** et **publication**, et la nécessité d’une **table de redirection** quand les slugs changent. J’ai aussi normalisé l’UX du plugin autour d’une page unique d’administration WordPress, ce qui est cohérent avec l’usage de `add_menu_page()` pour créer un point d’entrée dédié dans le backoffice. Enfin, le choix de spaCy pour les entités nommées et de `wbsearchentities` pour la découverte Wikidata est aligné avec les capacités documentées de ces outils. [codeable](https://www.codeable.io/blog/wordpress-taxonomy-url/)

## Prochaine étape utile
Je peux maintenant te produire l’un des trois livrables suivants :
1. un **README technique** plus compact pour le dépôt,
2. un **schéma SQL** complet des tables du plugin,
3. une **version prête pour Claude Code** avec consignes d’implémentation, architecture, fichiers attendus et ordre de travail.

Voulez-vous que je transforme ce `claude.md` en une version encore plus **opérationnelle pour l’implémentation**, avec structure de dossiers et tâches par fichier ?


# PROMPT_1
Peux-tu écrire un fichier claude.md pour ce projet, en organisant les éléments et en les amendant au besoin. Le développement de pipeline et du plugin sera ensuite fait à l'aide de claude code.

## OBJECTIF : 

1. Via une pipeline en python, classer les tags des posts issues d'un WordPress (taxonomy=post_tag, taxonomy=category) automatiquement afin de construire un fil d'ariane et validé son enrichissement Wikidata et Spacy (entités nommés). La finalité de la pipeline est de manipuler ensuite via un pugin dans le backoffice de WP ces tags des posts (taxonomy=post_tag, taxonomy=category) afin d'afficher ensuite un fil d'ariane optimisé.


3. Il faut pouvoir dans le plugin simuler le fil d'ariane, la traduction,, l'enrichissement, le slug  avant de valider le changement en production d'un tag issu du taxonomy=post_tag et taxonomy=category parce que c’est une création automatique qui peut être validé editorialement.

- Comme le fil d'ariane est une création ad hoc je peux stocker ces changement dans une table mysql additionnelle liés au plugin, ne pas hésiter à préserver les éléments originaux. Ce plugin doit etre disponible sur une destination unique du type /wp-admin/admin.php?page=breadcrumb-migration

- UX possible du plugin : Mapping element originaux (colonne de gauche) et éléments modifiés   (colonne de droite) avec tous les éléments pour opérer le changement optimisé afin de produire  le fil d'ariane, la traduction,, l'enrichissement, le slug  avant de valider le changement en production d'un tag issu du taxonomy=post_tag et taxonomy=category


3. Il existe un docker complet du wordpress avec l'ensemble de la base du wordpress afin  d'avoir un environnment de staging.


## RÉGLES

### 1. GROUPE PRIMAIRE
Tag catégorie
Les tags issus de taxonomy=category

- Sous-Rubrique
ex: Home › AI 


- IMPACT SUR URL ET BREADCRUMB
URL : Voir si je renomme les url via le label et le slug, il faudrait que je puisse faire une table de redirection.

URL: https://flaven.fr/category/ux-experience-utilisateur/ (KO)
URL: https://flaven.fr/category/ux-user-experience/ (OK)
Breadcrumb: Home › UX

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



