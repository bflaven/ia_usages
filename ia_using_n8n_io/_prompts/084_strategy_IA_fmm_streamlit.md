
# 083_strategy_IA_fmm.md

## INPUT_1
As a python expert, write the streamlit script named `streamlit_query_ollama.py` that will go on the top of the script `query_ollama.py` and `config.py`so as a user I can update the values `cms_section_keywords_list`, `lang`, `content`.

You must find for the variables`cms_section_keywords_list`, `lang`, `content` the proper type of streamlit element to simplify the UX of the user. Like I said before, the main objective remains to help me to update the values into the file config.py to launch the script easily with new values but this time through a streamlit application. 



## INPUT_2
Ok you enable the edit of the `config.py` can you add the save of the old `config.py` with a named like `config_[timestamp].py` and save the new config into `config.py`

## INPUT_3
Ok you have integrated the save can you launch directly from streamlit the `query_ollama.py` with the new config.


## INPUT_4
Change the last version of the script with following changes :
1. remove `cms_section_keywords_list` from the streamlit app. It is to be managed with the variable `lang` and the selection will be made into `config.py` with the help of case according to the language selected. So write the code that work for config and enable the select with the help of variable `lang`.

```python
FR_cms_section_keywords_list = """
Sports, Économie / Technologie, Culture, Environnement, France, Europe, Afrique, Amériques, Asie-Pacifique, Moyen-Orient
"""

ES_cms_section_keywords_list = """
América Latina, EE.UU. y Canadá, Europa, Francia, Asia-Pacífico, Medio Oriente, África, Medio Ambiente, Cultura, Economía, Ciencia y Tecnologías, Deportes
"""

EN_cms_section_keywords_list = """
France, Africa, Middle East, Americas, Europe, Asia-Pacific, Environment, Business / Tech, Sport, Culture
"""
```
2. Add the variable prompt into the streamlit script

```python
# Prompt template variable
prompt_template = """
En vous inspirant des exemples de titres suivants et en adoptant le profil d'un journaliste expérimenté spécialisé dans l'actualité internationale, générez un objet JSON valide strictement conforme aux spécifications ci-dessous à partir du {{content}} fourni par l'utilisateur. Le journaliste est un professionnel rigoureux, doté d'un sens aigu de l'éthique et d'une grande curiosité pour les affaires mondiales. Il est connu pour sa capacité à rendre accessibles des sujets complexes, tout en respectant les nuances culturelles et politiques. Aucune balise de code ou formatage supplémentaire n'est autorisée. La sortie doit être un objet JSON strict pouvant être consommé directement par une API, sans texte explicatif, sans balises ou tout autre format additionnel.

Lorsque le contenu aborde plusieurs thématiques, choisissez celle qui est le plus largement développée dans le contenu figurant dans {{content}}. Développez une problématique sur cette thématique principale, puis citez plus rapidement les autres sujets ou les thématiques secondaires en les distinguant bien de la première thématique.

Exemples de titres :
1. Japon : le combat des pères pour la garde partagée
2. Le successeur du Dalaï-lama sera désigné après sa mort, la Chine veut approuver son nom
3. Ibn Battuta, l'explorateur marocain qui "fait passer Marco Polo pour un flemmard"
4. DJ Snake et Omar Sy dévoilent "Patience", l'épopée "universelle" d'un jeune exilé sénégalais
5. Trump a-t-il raison de dire que l'article 5 de l'Otan peut "s'interpréter de plusieurs façons" ?
6. Washington cesse de livrer certaines armes à l'Ukraine, Kiev convoque le chargé d'affaires américain
7. Emmanuel Grégoire, le socialiste qui rêve de succéder à Anne Hidalgo à Paris
8. Fuites, pollutions, prix… En Outre-mer, une "discrimination environnementale" dans l'accès à l'eau

Format attendu du JSON :
1. "1" : Un titre en {{ lang }} journalistique créatif, pertinent, engageant, riche en mots-clés et adapté à une diffusion sur internet et les réseaux sociaux, pour un média d'actualité internationale. Le titre doit être rédigé en {{ lang }} et respecter les règles typographiques de la presse en {{ lang }} : seule la première lettre du titre doit être en majuscule, les autres lettres en minuscules (sauf noms propres). Les titres doivent comporter entre 50 et 60 caractères (espaces compris). Le titre peut contenir une touche d'humour, mais doit toujours refléter fidèlement le contenu, sans sensationnalisme. Puisqu'il traite de l'actualité internationale, les indications de pays ou de régions sont à privilégier dans les mots-clés de ces titres.
2. "2" : Un résumé complet en {{ lang }} et concis de 8 à 10 phrases des points principaux du texte, avec 1 ou 2 mots-clés inclus pour susciter l'intérêt du lecteur. Ce résumé doit faire entre 600 et 1000 caractères, avec une préférence pour 800 caractères. Il doit résumer la thématique principale en développant une problématique sur cette thématique, sans dévoiler tous les détails, afin de susciter l'intérêt du lecteur, mettre en avant l'angle principal de l'article, en étant à la fois informatif et incitatif. Adopter un ton professionnel, clair, structuré, précis et pédagogique, adapté à un grand public exigeant. Intégrer, si pertinent, une citation ou un chiffre marquant tiré du texte, pour renforcer l'accroche et l'intérêt du chapeau. Citez ensuite les autres sujets ou thématiques secondaires en les distinguant bien de la première thématique. Pour accroître la pertinence sur la thématique principale, posez une ou deux questions rhétoriques qui invitent le lecteur à réfléchir davantage sur le sujet principal. Abordez les thématiques secondaires sous forme de questions pour susciter la curiosité du lecteur et l'inciter à lire l'article complet.
3. "3" : Un tableau de quatre à sept mots-clés ou expressions les plus pertinents du texte, que les lecteurs potentiels utiliseraient pour le rechercher. Ces mots-clés doivent être en {{ lang }}.
4. "4" : Un tableau contenant une ou plusieurs catégories en {{ lang }} à laquelle appartient le contenu, choisies strictement parmi la liste suivante : {{ cms_section_keywords_list }}. La catégorie doit être en {{ lang }} et refléter la localisation géographique ou la thématique principale du contenu.

Le résultat doit être en {{ lang }} et structuré en JSON strictement comme suit :
{
  "1": "Titre de l'article 1",
  "2": "Résumé de l'article en 8-10 phrases.",
  "3": ["Mot-clé 1", "Mot-clé 2", "Mot-clé 3", "Mot-clé 4", "Mot-clé 5"],
  "4": ["Catégorie 1", "Catégorie 2"],
}

Assurez-vous que la catégorie choisie dans le champ 4 est bien dans la langue c'est à dire en {{ lang }} et que le format de sortie est strictement respecté. Ne fournissez que l'objet JSON pur en {{ lang }}, sans aucune balise, texte explicatif, ou autre formatage non JSON. Le résultat doit être un JSON brut et valide, strictement conforme aux spécifications, prêt à être consommé par une API.
"""
```
3. Add the management of the `# Output configuration
OUTPUT_FILE = "001a_ner_mistral_f24_fr_focus_mz508039.json"  # File to save the JSON response` with just the first part of the filename e.g 001a_ner_mistral_f24_fr_focus_mz508039.
4. Keep the content as a variable `content`




