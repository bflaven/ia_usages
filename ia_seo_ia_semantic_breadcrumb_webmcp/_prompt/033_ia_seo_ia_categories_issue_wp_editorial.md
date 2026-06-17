 ```text

 analyse, documentaire, Flash, flv, Intended Consequences, Jonathan Torgovnik, MediaStorm, technique

 
apache, CodeIgniter, Framework, Kohana, Linux, OOP, PHP, PHP5


actionscript, documentaire, Flash, Gaza, Israël Analyse, mov, Palestine, reportage, Sderot, technique


Adobe, apache, cloud computing, Ecology, Flash, Google, HTML5, Linux, PaaS, SaaS


.htpasswd, apache, Hébergement, Htaccess, Linux, mot de passe, protection répertoire
amour, Cyril Slucki, Ela & Dimitri, Lise Couzinier, temporalité, Transmedia, TransmediaLove



Agathe Films, Bruno Masi, Chechnya, Chernobyl, Cosaques, Crimea, documentaire, Gaité lyrique, Georgia, Guillaume Herbaut, Iran, La Montaña, La Zone, Lemonde.fr, livre, multimédia, Oeil Public, Ossetia, photographe, photojournaliste, Pripyat, Putin, ransmedia, révolution, russia, St Petersburg, Twitter, Webdocumentaire
```


```text
Zeplin is a tool that helps you push ready-to-build designs, automate workflows, and build products faster. It connects design, development, and product teams across functions, lifecycles, and geographies.


YSlow is a tool that grades web pages based on Yahoo!'s rules for high performance web sites. It offers suggestions, statistics, and tools for improving the page's speed and efficiency across various browsers and platforms.
```
```text
Wwwhatsnew

Wwwhatsnew.com is a technology media outlet founded in 2005 by Juan Diego Polo, a technology consultant with extensive experience in telecommunications engineering, IT project management, and web technology consulting.


Wwwhatsnew.com es un medio de tecnología fundado en 2005 por Juan Diego Polo, consultor tecnológico con una amplia trayectoria en ingeniería de telecomunicaciones, gestión de proyectos de TI y consultoría en tecnología web.

https://wwwhatsnew.com/
```


```text
Label:
Wwwhatsnew

Aliases:
Wwwhatsnew.com | WWWhatsnew | What's New | Wwwhatsnew tech blog |
Wwwhatsnew magazine

Description:
Spanish-language technology media outlet and blog founded in 2005 by
Juan Diego Polo, covering internet tools, web applications, digital
innovation and emerging technologies.

---

Subclass of (P279):
- technology blog (Q17442446)
- online magazine (Q1002697)
- digital media (Q1197685)

---

Uses (P2283):
- WordPress (Q10135)
- web publishing (Q) → may need to be created
- RSS (Q91565)
- social media (Q202833)

---

Founder (P112):
Juan Diego Polo → search:
https://www.wikidata.org/w/index.php?search=Juan+Diego+Polo
May need to be created as a new item.

Country of origin (P495):
Spain (Q29)

Language of work or name (P407):
Spanish (Q1321)

Inception (P571):
2005

Official website (P856):
https://wwwhatsnew.com/

---

Disambiguation strategy:
- Search before creating:
  https://www.wikidata.org/w/index.php?search=Wwwhatsnew
- Unusual name with triple-w spelling reduces collision risk.
- Must be distinguished from generic "what's new" pages or
  software changelog entries.
- Use label "Wwwhatsnew" preserving exact brand spelling as
  primary disambiguating anchor.
- Add instance of (P31) → online newspaper (Q1153191) or
  technology blog (Q17442446) as primary anchor claim.
- Add founder (P112) → Juan Diego Polo to reinforce identity.
- If Juan Diego Polo has no QID, create his item first with:
  instance of (P31) → human (Q5)
  occupation (P106) → technology consultant (Q) / blogger (Q4854788)
  country of citizenship (P27) → Spain (Q29)
```

## PROMPT_4


I need a better UX for the plugin `Breadcrumb Migration Version 1.27.0`, through use, I discovered that the plugin needs improvements. Here are the changes needed that should take into account these observations.


It affect the all workflow but i need to improve the other way round. The plugin has the main objective to improve SEO on tags by enriching with wiki and entity but sometimes `Description from Wikidata` does not exist because most of the time the `Wikidata ID` does not exist. It is time consuming to create an item on wikidata e.g I gave you two examples below : `Zeplin` so the value in `Actual Description` has been hand written by me. I need to trace the process back to indicate this information because I absolutely must keep this handwritten description.

1. In the tab "Proposals", regardless of the states of the tag (Pending, Approved, Rejected), I need to be able to correct/update so that edit and save to flag that the tag is hand written so for instance I can empty the "Description" for the moment. It does not work, if I empty the description, it is not taken into account.
e.g in `Zeplin` the `Description from Wikidata` and  `Wikidata ID` are wrong so I want to empty and maybe call the one stored in WP and flag as `✍ Written`. Give me the best UX with communication.

2. In the tab "Bulk Description", in column Actual Description for each tag,  you can add a button `→ Copy to Wikidata` that will copy the wp description and flag as `✍ Written` when I will come back on the same item in the tab "Proposals".

3. If for instance, someone decide to create the wikidata item on wikidata e.g `Zeplin` I can fill back the `Wikidata ID` fetch the `Description from Wikidata` and overwrite the `Actual Description` if it is a sensible editorial decision if I decide to do so.

NOTE: Before coding, summarize in bullet points that you understand from the given instructions. Update the readme in the changelog in the readme and the version of the script when I validate the changes asked.






## PROMPT_3

```text
web components, web content, web design, Web Application
```


Q258394 already exists on Wikidata. Here is what to CHECK and potentially ADD or IMPROVE on that item.

```text
Label:
web marketing (Q258394)
https://www.wikidata.org/wiki/Q258394

---

ACTION: EDIT the existing item, do not create a new one.
Navigate directly to:
https://www.wikidata.org/wiki/Q258394

---

Aliases to ADD if missing:
online marketing | digital marketing | internet marketing |
e-marketing | web advertising | online advertising

---

Description to VERIFY or IMPROVE:
Practice of promoting and selling products or services using
internet-based digital channels including search engines, social
media, email, and websites.

---

Subclass of (P279) — ADD if missing:
- marketing (Q39809)
- digital media (Q1197685)
- electronic commerce (Q44689)

---

Uses (P2283) — ADD if missing:
- search engine optimization (Q180711)
- social media (Q202833)
- email marketing (Q1152977)
- content marketing (Q4984539)
- pay-per-click (Q751571)
- web analytics (Q1326488)

---

Official website (P856):
No single official URL for this concept.
Use reference URL (P854) pointing to a reputable source:
https://en.wikipedia.org/wiki/Online_advertising

---

Disambiguation strategy:
- Q258394 already exists — focus on improving existing claims.
- Must be distinguished from:
  marketing (Q39809) → broader concept, not internet-specific
  advertising (Q37038) → broader traditional concept
  digital marketing (Q) → near-synonym, check if separate QID exists
- Use different from (P1889) → marketing (Q39809) to make
  the internet-specific scope explicit.
- Verify existing description is in English and clearly states
  "internet-based" as primary disambiguating term.
- Check if digital marketing has its own QID and link via
  said-to-be-the-same-as (P460) or different from (P1889)
  depending on editorial consensus.
```


## PROMPT_2
I need a better UX for the plugin `Breadcrumb Migration Version 1.26.0`, through use, I discovered that the plugin needs improvements. Here are the changes needed: 

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