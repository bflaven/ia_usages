
## PROMPT_2

Write a new script 002_parsing_tags_similarity_sqlite_export_sqlite_csv.py that will do the 2 objectives that you describe:
1. Add clustering/HDBSCAN on embeddings to define families.
2. Add entity type info (from NER) and usage_count to choose canonical tags.

The build the WordPress plugin that imports related_tags_embeddings_settings_csv_1.csv into a custom table and exposes it in tag edit screens and front‑end templates will be made later. Focus on the 2 objectives above.


## PROMPT_1

Rewrite the file 001_parsing_tags_similarity_sqlite_export_sqlite_csv.py. I gave you the structure of the json file. For the moment the script does not grab any tag.
```json
[
  {
    "id": 1570,
    "count": 1,
    "description": "",
    "link": "https://flaven.fr/tag/18daysinegypt/",
    "name": "#18DaysInEgypt",
    "slug": "18daysinegypt",
    "taxonomy": "post_tag",
    "meta": [],
    "_links": {
      "self": [
        {
          "href": "https://flaven.fr/wp-json/wp/v2/tags/1570",
          "targetHints": {
            "allow": [
              "GET"
            ]
          }
        }
      ],
      "collection": [
        {
          "href": "https://flaven.fr/wp-json/wp/v2/tags"
        }
      ],
      "about": [
        {
          "href": "https://flaven.fr/wp-json/wp/v2/taxonomies/post_tag"
        }
      ],
      "wp:post_type": [
        {
          "href": "https://flaven.fr/wp-json/wp/v2/posts?tags=1570"
        },
        {
          "href": "https://flaven.fr/wp-json/wp/v2/clients?tags=1570"
        }
      ],
      "curies": [
        {
          "name": "wp",
          "href": "https://api.w.org/{rel}",
          "templated": true
        }
      ]
    }
  }
]
```




## OUTPUT_1






