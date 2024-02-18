# usecase_2_text_classification

**Le dispositif effectif qui s'appuie sur Mistral via Ollama (prompt) et va générer un CSV via pandas pour récupérer en sortie chaque post tagué avec une des catégories FRANCE24.**

A l'aide de ce dispositif de recatégorisation, c’est un POC notamment c’est gratuit et  sécurisé puisque Mistral a été substitué à ChatGPT 


Le CSV sur USECASE_2 est sur le ticket. Il possède les colonnes suivantes.

-- **Message :** le message d’origine qui vient de ton csv. Texte en FR.

-- **category_predicted :** la catégorie en anglais deviné par mistral sur la base de ma proposition dans le prompt

-- **category_decision :** le commentaire en anglais de la décision de mistral que j’ai inclus dans le prompt


- **Objectif :** Catégorisation des posts des RS à rapprocher de la catégorisation des posts de FMM (F24, RFI, MCD). La même catégorisation qui sert aux tracking des posts consommés sur les environenements.
- **Ticket :** https://francemm.atlassian.net/browse/IA-39
- **Source :**Voir dera-usecases/usecase_2_text_classification/data_split/bronze_dataset_source/source_all_published_posts_table_1.csv
- **Abstract :** usecase_2 (IA-39) catégorisation des posts par l’équipe des réseaux sociaux (usecase_2_text_classification)


