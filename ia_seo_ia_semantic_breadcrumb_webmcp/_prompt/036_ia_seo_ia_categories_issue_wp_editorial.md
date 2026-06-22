##  PROMPT_1
As an python developper, editorial responsible and as the editor of a personal blog. 


1. Read `MODEL_007_poc_api_dtsi.py` to leverage on this script to write a script named `001_complete_breadcrumb_migration.py`

2. The script named `001_complete_breadcrumb_migration.py` should read the file
`source/breadcrumb_migration_bulk_description_20260622_145542.json` find the items where `"actual_description": "",` is empty. Count the number of items where this requirement is true. Print the `tag_name`, just to ensure visually that these items are empty.

3. Based on `tag_name` write, in english, with the help of api key in the env, a wikidata description for each item and output in a json file  `destination/filed_[timestamp]_breadcrumb_migration_bulk_description_20260622_145542.json`


4. Use the env "ia_achats" made with conda that is already existing in the machine.





--- extract from `source/breadcrumb_migration_bulk_description_20260622_145542.json`
```json
{
    "tag_name": "Nitendo Wii",
    "proposed_slug": "nitendo-wii",
    "wp_term_id": "260",
    "wikidata_id": "",
    "wikidata_description": "",
    "actual_description": "",
    "desc_source": "empty"
  },
```
--- output the same extract in `destination/breadcrumb_migration_bulk_description_20260622_145542.json` where the actual description should be filled in English.
```json
{
    "tag_name": "Nitendo Wii",
    "proposed_slug": "nitendo-wii",
    "wp_term_id": "260",
    "wikidata_id": "",
    "wikidata_description": "",
    "actual_description": "The Wii is a home video game console produced by the Japanese manufacturer Nintendo between 2006 and 2013. It is part of the seventh generation of consoles, just like Microsoft's Xbox 360 and Sony's PlayStation 3.",
    "desc_source": "empty"
  },
```


NOTE: Before coding, summarize in bullet points that you understand from the given instructions. Update the readme in the changelog in the readme and the version of the script when I validate the changes asked.






