
## PROMPT_4

1. In the tab "Delta — New Tags", make the change for the language I want in english. Add it as a settings in the plugin e.g https://www.wikidata.org/w/index.php?search=Palantir&language=en

2. When I publish a tag with a correct category, I want to be able to update the Description for instance because it will be shown on the tag result page like for the category. For the moment, I can only do it when I publish for the first time and then I cannot change or update the description.

Summarize your comprehension before coding.






## PROMPT_3
In the tab "Delta — New Tags", can you help to perform the search with the Wikidata label e.g Palantir in to find the Wikidata ID e.g Q2047336 for instance to grab more easily the Wikidata ID

The direct link to Wikidata should open in a target blank, if you make a link, so I do not quit the wp admin it will open a new tab in the browser e.g https://www.wikidata.org/w/index.php?search=Palantir&language=fr

Summarize your comprehension before coding.

## PROMPT_2

What can I do with the delta especially for the post_tag items. Let's say i have a file 2000 tags, but I have added 25 new tags. How can add directly within the plugin, have the delta and complete manually? I will do the step_2, step_3 manually to determine the name entity and the enrichment via wikidata so I can complete the new tags and then do my breadcrumb migration.

1. The plugin live in `_ia_seo_ia_semantic_breadcrumb/wp-plugin-breadcrumb-migration`.

2. Do not make something complex in the plugin, I just want to do it manually.
- list the tags that you do have both in post_tag
- then enable for each new tag the step_2 and step_3 manually.

3. Summarize your comprehension before coding in `_ia_seo_ia_semantic_breadcrumb/wp-plugin-breadcrumb-migration`








## PROMPT_1

Create a WP (wordpress) plugin that enable to select to export all the post_tag (post_tag) or all the categories (category) both in in json or in csv.
The plugin should enable be to :
- select the output format: json or csv
- select the type of taxonomy: category or post_tag
- select the type of taxonomy: total_processed and limit
- select the mode dry_run : true or false. True it is just a simulation, False it is made for real and out the file.
- For category, the filename ouptut should be for `category_[timestamp]_step_1_inventory.csv` or `category_[timestamp]_step_1_inventory.json` with the structure given below.
- For post_tag, the filename ouptut should be for `post_tag_[timestamp]_step_1_inventory.csv` or `post_tag_[timestamp]_step_1_inventory.json` with the structure given below.

Summarize your comprehension before coding.

Note: I want to cut and paste, use best practices for WP plugin, dry... etc

**`category_[timestamp]_step_1_inventory.csv`**
```text
taxonomy,id,name,slug,post_count,parent_id
category,219,Accessibilité,accessibilite,26,0
```

**`category_[timestamp]_step_1_inventory.json`**
---  

```json
{
  "timestamp": "2026-05-10T18:36:00.244144+02:00",
  "pipeline_step": "inventory",
  "taxonomy": "category",
  "total_processed": 1,
  "config": {
    "limit": 1,
    "dry_run": false,
    "taxonomy": "category"
  },
  "data": [
    {
      "id": 219,
      "name": "Accessibilité",
      "slug": "accessibilite",
      "taxonomy": "category",
      "post_count": 26,
      "parent_id": 0
    }
  ]
}
```
`post_tag_[timestamp]_step_1_inventory.csv`
```
taxonomy,id,name,slug,post_count,parent_id
post_tag,1570,#18DaysInEgypt,18daysinegypt,1,0
```

`post_tag_[timestamp]_step_1_inventory.json`
```json
{
  "timestamp": "2026-05-10T14:41:21.814517+02:00",
  "pipeline_step": "inventory",
  "taxonomy": "post_tag",
  "total_processed": 1,
  "config": {
    "limit": 1,
    "dry_run": false,
    "taxonomy": "post_tag"
  },
  "data": [
    {
      "id": 1570,
      "name": "#18DaysInEgypt",
      "slug": "18daysinegypt",
      "taxonomy": "post_tag",
      "post_count": 1,
      "parent_id": 0
    }
  ]
}
```