
## using the template
```bash
# some random words from tags
Wolof, Wordpress, Yoruba, Zulu
```





## PROMPT_2
Can you update the plugin in this directory so 

1. It extends these Sapcy name entities with the list below. You can add the all list in the drop-down everytime the drop-down is called.


2. In tab "Settings", you can add the list so I know whate these Sapcy name entities are. 


```html
<select name="spacy_entity">...</select>
``` 

```text
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
```
Caution: Summarize your comprehension before coding and make a full bullet proposition step by step. Do not forget to update the readme and the plugin version.

## PROMPT_1
Can you update the plugin in this directory so that in the tab "Proposals", in the space "bm-col bm-col--proposed", when I click on edit. I should be able to have access to the following fields:


1. Field Label so I can edit and update. If I change it before or after publishing, it should save my changes.

2. Field spaCy so I can edit and update. If I change it before or after publishing, it should save my changes. It should load this select :
```html
<select name="spacy_entity"><option value="">— none —</option><option value="PERSON">PERSON</option><option value="ORG">ORG</option><option value="GPE">GPE</option><option value="LOC">LOC</option><option value="PRODUCT">PRODUCT</option><option value="EVENT">EVENT</option></select>
```
3. Field Wikidata ID so I can edit and update. If I change it before or after publishing, it should save my changes.

Caution: Summarize your comprehension before coding and make a full bullet proposition step by step. Do not forget to update the readme and the plugin version.


