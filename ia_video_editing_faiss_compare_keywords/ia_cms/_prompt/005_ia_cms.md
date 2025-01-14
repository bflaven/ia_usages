
# 005_ia_cms.md

## PROMPT_1

As python expert can you write a script that:
- loads a file name "pt_tags_thema_list_2.json" like below 
- ouputs all the keyword in a variable named "cms_existing_kw" like below, in a pyhton list.



```json
{
    "nid": "959cf240-aa97-11e8-9830-005056a9425e",
    "created": 1535442866,
    "changed": 1582565211,
    "type": "taxonomy",
    "description": "keywords in Portuguese",
    "keywords": [
        {
            "code": "105_D64_8802",
            "libelle": "\"Milagre económico\"",
        },
        {
            "code": "105_D64_8876",
            "libelle": "\"agentes do estrangeiro\"",
        },
        {
            "code": "105_D64_MZ25210",
            "libelle": "\"persona non grata\".",
        },
        {
            "code": "105_D64_8929",
            "libelle": "\"phygital\"",
        },
        {
            "code": "105_D64_MZ26026",
            "libelle": "",
        },
        {
            "code": "105_D64_9601",
            "libelle": "",
        },
        {
            "code": "105_D64_MZ54566",
            "libelle": "“FILIPO”",
        }
    ]
}
```

```python

cms_existing_kw = ["Milagre económico", "agentes do estrangeiro", "phygital"]

```

## PERPLEXITY_1
Certainly! Here's a Python script that loads the JSON file "pt_tags_thema_list_2.json" and extracts all the non-empty keywords into a list named `cms_existing_kw`:

```python
import json

# Load the JSON file
with open('pt_tags_thema_list_2.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Extract non-empty keywords
cms_existing_kw = [
    keyword['libelle'].strip('"')
    for keyword in data['keywords']
    if keyword['libelle'].strip('"')  # This condition excludes empty strings
]

# Print the result
print("cms_existing_kw =", cms_existing_kw)
```

This script does the following:

1. It imports the `json` module to handle JSON data.
2. It opens and reads the "pt_tags_thema_list_2.json" file.
3. It uses a list comprehension to create `cms_existing_kw`:
   - It iterates through each keyword in the 'keywords' list.
   - It strips the quotation marks from the 'libelle' value.
   - It includes the keyword only if it's not an empty string after stripping.
4. Finally, it prints the resulting list.

When you run this script, it will output something like:

```python
cms_existing_kw = ["Milagre económico", "agentes do estrangeiro", "persona non grata", "phygital", "FILIPO"]
```

Note that this script:
- Removes the surrounding quotation marks from the keywords.
- Excludes any keywords that are empty strings.
- Includes all non-empty keywords, even if they weren't in your example output (like "persona non grata" and "FILIPO").

If you need to modify the output further (e.g., to exactly match your example), you can add additional filtering or processing steps.

