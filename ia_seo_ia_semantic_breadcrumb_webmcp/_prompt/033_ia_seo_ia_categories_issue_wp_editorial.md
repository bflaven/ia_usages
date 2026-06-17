

## PROMPT_2
I need a better UX for the plugin `Breadcrumb Migration Version 1.26.0`, through use, I discovered that the plugin needs improvements. Here are the chnages needed: 

1. In the tab "Proposals", regardless of the states of the tag (Pending, Approved, Rejected), I need to be able to correct/update so that edit and save the values in the following places to correct editorially each tag that I found incorrect as an a member of the editorial team.

1.1. In the column "ORIGINAL" `<!-- ORIGINAL column -->`, I need to be able to edit and save the following values:

- `Name`  
- `Slug`

1.2. In the column "PROPOSED" `<!-- PROPOSED column -->`, I need to be able to edit and save the following values:

- `Breadcrumb`


2. I am more explicit with true production example, there is a misspelling in the original tag e.g `webdocumentaires : gide de survie et conseils pratiques`, I have corrected it in WP with a tag edit action e.g `webdocumentaires : guide de survie et conseils pratiques`  but the original data is not editable and possible to update so the `proposed_breadcrumb` is wrong e.g `"proposed_breadcrumb": "[\"Home\",\"Digital Storytelling &amp; Webdocs\",\"webdocumentaires : gide de survie et conseils pratiques\"]",` I should be able to edit and save to `"proposed_breadcrumb": "[\"Home\",\"Digital Storytelling &amp; Webdocs\",\"webdocumentaires : guide de survie et conseils pratiques\"]",`. There are plenty of such errors.


- extract from `bm_proposals_20260617_055346.json`
```json

{
            "id": "2421",
            "term_id": "2421",
            "proposed_name": "webdocumentaires : guide de survie et conseils pratiques",
            "proposed_slug": "webdocumentaires-guide-de-survie-et-conseils-pratiques",
            "proposed_description": "",
            "proposed_parent_id": "3436",
            "proposed_language": "fr",
            "spacy_entity": null,
            "wikidata_id": null,
            "wikidata_label": null,
            "wikidata_description": null,
            "proposed_breadcrumb": "[\"Home\",\"Digital Storytelling &amp; Webdocs\",\"webdocumentaires : gide de survie et conseils pratiques\"]",
            "validation_state": "approved",
            "validated_by": "1",
            "validated_at": "2026-06-17 07:15:18",
            "created_at": "2026-05-12 17:23:09"
        },

```

NOTE: Before coding, summarize in bullet points that you understand from the given instructions. Update the readme in the changelog in the readme and the version of the script when I validate the changes asked.




## PROMPT_1
```text

Wordpress Mu, workshop, work, webdocu.fr, webdocumentaire traversée, webfiction

webdocumentary
```

```text
WordPress Multisite
Un réseau WordPress Multisite fonctionne en ajoutant une couche de contrôle au-dessus d’une installation WordPress standard. Il partage les ressources de base tout en conservant les données de chaque site séparément. Décortiquons les éléments clés.
```

```text
Label:
WordPress Multisite

Aliases:
WordPress Multisite | WP Multisite | WordPress Network | WordPress MU | WPMU

Description:
Built-in WordPress feature enabling a single WordPress installation to host
and manage a network of multiple independent websites, sharing core resources
while keeping each site's data separate.

---

Subclass of (P279):
- content management system (Q170021)
- web application (Q1330336)
- software feature (Q3966506)

---

Uses (P2283):
- WordPress (Q10135)
- PHP (Q59)
- MySQL (Q14357)
- Apache HTTP Server (Q11354) or nginx (Q1278515)
- multitenancy (Q1185663)

---

Official website (P856):
https://wordpress.org/documentation/article/create-a-network/

---

Disambiguation strategy:
- Search before creating:
  https://www.wikidata.org/w/index.php?search=WordPress+Multisite
- Must be distinguished from:
  WordPress (Q10135) → parent software, not the same item
  WordPress MU (historical predecessor, merged into WordPress 3.0)
- Use label "WordPress Multisite" not "WordPress Network" as primary
  label since "Multisite" is the official product terminology.
- Add part of (P361) → WordPress (Q10135) to anchor it as a
  sub-feature rather than a standalone product.
- Add instance of (P31) → software feature (Q3966506) as primary
  anchor claim to distinguish from WordPress itself.
- Add inception (P571) → 2010 (introduced in WordPress 3.0).
- Use different from (P1889) → WordPress MU (Q) if a legacy
  WordPress MU item exists, to clarify historical succession.
```