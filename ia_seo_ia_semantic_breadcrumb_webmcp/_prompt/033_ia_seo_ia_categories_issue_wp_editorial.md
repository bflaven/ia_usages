
## PROMPT_19

Do not make any development this time inside the plugin. This is temporary work. I want to take advantage of your ability to categorize tags in a single main category base on you understanding. If the tag is unkwon, put it in `Miscellaneous / Other` 

1. Can you make a quick bulk assignment for each tag inside `breadcrumb-migration`.
- Here is the categories in `sample_categories_1.txt`
- Here is the tags in `sample_pending_tag_1.txt`

You can output the result in a file `sample_tags_assigned_categories_1.txt` like so, with the same structure I want a quick and dirty cut and paste. One tag can only belong to one category. Goctha ?

- future file `sample_tags_assigned_categories_1.txt`
```text
// AI & Machine Learning
AI Product Owner, AI takeover... etc


// Digital Storytelling & Webdocs
Honky Tonk, honkytonk, honkytonk films... etc

// Miscellaneous / Other
[nothing that you know, so it is the same for me !]

```

NOTE: Before coding, summarize in bullet points that you understand from the given instructions. Update the readme in the changelog in the readme and the version of the script when I validate the changes asked.



## PROMPT_18

I need a better UX for the plugin `Breadcrumb Migration Version Version 1.32.0`, through use, I discovered that the plugin needs improvements. Here are the changes needed that should take into account these observations.

1. The files are in `breadcrumb-migration`.

2. In the tab "Proposals", I need to know the exact list of tag for each status `Pending`, `Approved`, `Rejected` if I click on one of the word then it should a new area with 3 buttons and textarea make it look like wp stuff e.g
`<span class="bm-stat bm-stat--pending"><strong>1930</strong> Pending</span>` I should be able grab a comma separated list e.g `Trump, Obama, Wordpress, IA` of the tags in this status in a textarea that need to be created, you can give a name to this section above "Bulk Keyword Search" and under "Overview".
Why because I am wasting my time look for tags, I need to leverage on bulk operations available in the other tabs and through a list of tag selected.

- Actual counting for the tags status
```text
1581 Pending
1021 Approved
5 Rejected
```

NOTE: Before coding, summarize in bullet points that you understand from the given instructions. Update the readme in the changelog in the readme and the version of the script when I validate the changes asked.












## PROMPT_15

```text
2012, Alexis Sarini, Antonin Lhôte, atelier, atelier desmédias, bruxelles, CFPJ, CFPJ Médias, Damien Van Achter, data, Data journalism, data journalisme, davanac, davanac.net, Eghezée, équipe de campagne, éric schérer, étudiants, formation, François Hollande, futur, IHECS, initiation, marie coussin, master class, masterclass, Namur, open newsroom, organigramme, owni.fr, Parti Socialiste, politique, présidentielle 2012, presse, Primaires, Primaires Socialistes, PS, richmedia, Studio Hans Lucas, UMP


#mc11, #mc12, #mc13, 17 octobre 1961, 2012, 3WDOC, 3WDOC Studio, Alexis Sarini, Algérie, Antonin Lhôte, atelier, atelier desmédias, belgique, bruxelles, CFPJ, CFPJ Médias, Dailymotion, Damien Van Achter, data, Data journalism, data journalisme, davanac, davanac.net, Eghezée, EMI-CFD, équipe de campagne, éric schérer, étudiants, formation, François Hollande, futur, guerre d'Algérie, HTML5, IHECS, initiation, journalisme, La nuit oubliée, Lemonde.fr, marie coussin, master class, masterclass, Namur, Olivier Lambert, open newsroom, organigramme, Owni, owni.fr, Parti Socialiste, politique, présidentielle 2012, presse, Primaires, Primaires Socialistes, PS, reportage, richmedia, Studio Hans Lucas, Thomas Salva, Twitter, UMP, Virginie Terrasse, webdocu, webdocu.fr, webjournalisme, Wilfrid Estève, workshop
```







## PROMPT_14
Create 002_wikidata_api_add_item.py that take into account the claims e.g subclass_of, uses... etc

```text
# SANDBOX (safe, use this first)
# create the item
python 001_wikidata_api_add_item.py --item data/item_3WDOC.yaml --sandbox --no-claims

# create the item with the claims
python 001_wikidata_api_add_item.py --item data/item_Zeplin.yaml --sandbox



# PRODUCTION 
# dry-run
python 001_wikidata_api_add_item.py --item data/item_Zeplin.yaml --dry-run

# go for it
# write to production

python 001_wikidata_api_add_item.py --item data/item_Zeplin.yaml
```



```yaml
# item_zeplin.yaml

label_en: "Zeplin"

description_en: "web-based collaboration platform connecting design, development and product teams by transforming ready-to-build designs into automated workflows and developer handoff assets"

aliases_en:
  - "Zeplin app"
  - "Zeplin design handoff"
  - "Zeplin collaboration tool"
  - "Zeplin design to development"

subclass_of:
  - label: "web application"
  - label: "collaborative software"
  - label: "software as a service"

uses:
  - label: "design handoff"
  - label: "Figma"
  - label: "Sketch"
  - label: "Adobe XD"

official_website: "https://zeplin.io/"
```


## PROMPT_13
Generate a wikipedia and also replace the elemnts in the template YAML below

```text
Zeplin

Zeplin is a tool that helps you push ready-to-build designs, automate workflows, and build products faster. It connects design, development, and product teams across functions, lifecycles, and geographies.
```

```yaml
# item_template.yaml — copy this file and rename it for your item
# Example:  cp data/item_template.yaml data/item_myproject.yaml
#
# Edit only the VALUES — do NOT rename any key (label_en, label, qid, etc.)
# Lines starting with # are comments and are ignored by the script.
#
# HOW TO USE:
#   1. Copy:   cp data/item_template.yaml data/item_myproject.yaml
#   2. Fill in all FILL_ME_IN values below
#   3. Test:   python 001_wikidata_api_add_item.py --item data/item_myproject.yaml --sandbox --no-claims
#   4. Check the printed QID resolutions, fix any wrong matches in your YAML
#   5. Dry-run: python 001_wikidata_api_add_item.py --item data/item_myproject.yaml --dry-run
#   6. Produce: python 001_wikidata_api_add_item.py --item data/item_myproject.yaml

# ── Basic information ─────────────────────────────────────────────────────────

# Short name shown as the title on Wikidata (keep it short, no period)
label_en: "FILL_ME_IN"

# One sentence — no capital letter at start, no period at the end
description_en: "FILL_ME_IN short description of the item"

# Other names people use for this item (one per line, each line starts with -)
# Remove lines you do not need, or add more
aliases_en:
  - "FILL_ME_IN alias 1"
  - "FILL_ME_IN alias 2"

# ── Statements (claims) ───────────────────────────────────────────────────────
# You do NOT need to know the QID — just write the English label.
# The script searches Wikidata automatically and prints what it found.
# Check the printed output before running on production.
#
# To find good label names: search https://www.wikidata.org and copy the label text.
#
# If you DO know the exact QID, add:  qid: "Q12345"
# and it will be used directly without searching.
#
# Remove entries you do not need. Add more by copying a "- label:" block.

# P279 — "subclass of": what broader category does this item belong to?
subclass_of:
  - label: "FILL_ME_IN category name"
  - label: "FILL_ME_IN category name"

# P2283 — "uses": what technologies, tools, or languages does this item use?
uses:
  - label: "FILL_ME_IN technology name"
  - label: "FILL_ME_IN technology name"

# P856 — official website (must start with https://)
official_website: "https://FILL_ME_IN.com/"
```


## PROMPT_13
```text
University of the West of England

The University of the West of England, also known as UWE Bristol, is a public research university, located in and around Bristol, England, UK. With over 38,000 students and 4,500 staff, it is the largest provider of higher education in the South West of England. 
```

## A_PROMPT_12
```text
Label:
3WDOC

Aliases:
3WDOC Studio | 3WDOC Player | 3WDOC Editor | Three W Doc | WebDoc Studio |
HTML5 Webdocumentary Tool

Description:
Open-source HTML5 authoring and playback platform for creating and
delivering interactive rich media web stories and webdocumentaries,
combining a Studio editor with a Player for digital storytelling on the web.

---

Subclass of (P279):
- web application (Q1330336)
- multimedia authoring software (Q1420342)
- free and open-source software (Q341)
- digital storytelling tool (Q) → may need to be created

---

Uses (P2283):
- HTML5 (Q2053796)
- JavaScript (Q2005)
- rich media (Q1361745)
- webdocumentary (Q) → may need to be created
- digital storytelling (Q7325049)

---

Official website (P856):
https://3wdoc.com/

---

Disambiguation strategy:
- Search before creating:
  https://www.wikidata.org/w/index.php?search=3WDOC
- Low collision risk due to distinctive alphanumeric name.
- Add instance of (P31) → software (Q7397) as primary anchor claim.
- Add main subject (P921) → webdocumentary and digital storytelling
  to anchor thematic scope.
```

---

```yaml
# One sentence — no capital letter at start, no period at the end
description_en: "open-source HTML5 authoring and playback platform for creating interactive rich media web stories and webdocumentaries, combining a Studio editor with a Player for digital storytelling on the web"

# Other names people use for this item (one per line, each line starts with -)
aliases_en:
  - "3WDOC Studio"
  - "3WDOC Player"
  - "3WDOC Editor"
  - "Three W Doc"
  - "HTML5 Webdocumentary Tool"

# ── Statements (claims) ───────────────────────────────────────────────────────
# P279 — "subclass of"
subclass_of:
  - label: "web application"
    qid: "Q1330336"
  - label: "multimedia authoring software"
    qid: "Q1420342"
  - label: "free and open-source software"
    qid: "Q341"
  - label: "digital storytelling"
    qid: "Q7325049"

# P2283 — "uses"
uses:
  - label: "HTML5"
    qid: "Q2053796"
  - label: "JavaScript"
    qid: "Q2005"
  - label: "rich media"
    qid: "Q1361745"
  - label: "digital storytelling"
    qid: "Q7325049"

# P856 — official website
official_website: "https://3wdoc.com/"
```


## PROMPT_14
Generate a wikipedia and also replace the elemnts in the template YAML below

```text
3WDOC

3WDOC Studio is a versatile tool specificaly designed to create and deliver rich media experiences optimized in HTML5 to run across the web. The 3WDOC Player's ultimate goal is to enable one or several author(s) to create an authentic web story. 3WDOC Player is a versatile tool to create and deliver rich media experiences optimized in HTML5 to run across the web. This technology can be applied to any kind of rich media sites, like for instance for the emerging genre named webdocumentary. So naturally, here in 3WDOC, we summarize the project concept in this simple motto: "Facilitating the digital storytelling on the Web". 3WDOC Studio = 3WDOC Player + 3WDOC Editor."
```

```yaml
# One sentence — no capital letter at start, no period at the end
description_en: "FILL_ME_IN short description of the item"

# Other names people use for this item (one per line, each line starts with -)
# Remove lines you do not need, or add more
aliases_en:
  - "FILL_ME_IN alias 1"
  - "FILL_ME_IN alias 2"

# ── Statements (claims) ───────────────────────────────────────────────────────
# You do NOT need to know the QID — just write the English label.
# The script searches Wikidata automatically and prints what it found.
# Check the printed output before running on production.
#
# To find good label names: search https://www.wikidata.org and copy the label text.
#
# If you DO know the exact QID, add:  qid: "Q12345"
# and it will be used directly without searching.
#
# Remove entries you do not need. Add more by copying a "- label:" block.

# P279 — "subclass of": what broader category does this item belong to?
subclass_of:
  - label: "FILL_ME_IN category name"
  - label: "FILL_ME_IN category name"

# P2283 — "uses": what technologies, tools, or languages does this item use?
uses:
  - label: "FILL_ME_IN technology name"
  - label: "FILL_ME_IN technology name"

# P856 — official website (must start with https://)
official_website: "https://FILL_ME_IN.com/"
```



## PROMPT_13

```text
agentic browser

An agentic browser is an AI-powered web browser that can autonomously navigate websites, fill out forms, and complete tasks on behalf of the user, rather than just displaying content.
```

```text
Label:
agentic browser

Aliases:
agentic browser | AI browser agent | autonomous browser | AI-powered browser |
browser agent | web agent | agentic web browser

Description:
AI-powered web browser capable of autonomously navigating websites, filling
forms and completing multi-step tasks on behalf of the user, going beyond
passive content display toward goal-directed autonomous web interaction.

---

Subclass of (P279):
- web browser (Q6368)
- intelligent agent (Q2676249)
- artificial intelligence software (Q97508154)

---

Uses (P2283):
- large language model (Q107520748)
- natural language processing (Q30642)
- reinforcement learning (Q830687)
- web scraping (Q665452)
- computer vision (Q45977760)
- autonomous agent (Q2676249)

---

Official website (P856):
No single official URL — concept spanning multiple implementations.
Use reference URL (P854):
https://en.wikipedia.org/wiki/Browser_automation

---

Notable implementations — add has part (P527) or
different from (P1889) once QIDs exist:
- Operator (OpenAI)
- Atlas (OpenAI)
- Comet (Perplexity)
- Browser Use (open source)
- Convergence Proxy

---

Disambiguation strategy:
- Search before creating:
  https://www.wikidata.org/w/index.php?search=agentic+browser
- Existing item Q135456040 may already cover this concept —
  verify before creating a duplicate:
  https://www.wikidata.org/wiki/Q135456040
- Must be distinguished from:
  web browser (Q6368) → passive content display only
  browser automation (Q) → scripted automation, not AI-driven
  web crawler (Q680916) → indexing focus, not task completion
- Use different from (P1889) → web browser (Q6368) to make
  the autonomous AI distinction explicit.
- Add instance of (P31) → software (Q7397) and
  concept (Q151885) depending on whether item represents
  the concept or a specific implementation.
- Add main subject (P921) → autonomous agent (Q2676249)
  and artificial intelligence (Q11660) as thematic anchors.
```


## PROMPT_12
Ok with the change for v1.31.0
1. In the tab "Bulk Description". Error in row color for status (Completed, Incomplete, Empty). I have row Completed and they are NOT in the good color. Check color per status row and fiw.



## PROMPT_11
It is not exactly working like you describe. At least let me explain the possible workflow because we are talking about editorial with value not technical feature or function with no value ! Here is my understanding of what it should do. Humans are above machines.


Ok so I have edited  and updated the "Adobe" description like you said in the WP out of the scope of the `Breadcrumb Migration` plugin. It is now  a human written description in `Actual Description`. 
The real risk is that I overwrite the `Actual Description` with `Description from Wikidata` with the help of the `→ Copy to Actual` button when the `Wikidata ID` is existing. You have to know that I need to write hand-written `Actual Description` because `Wikidata ID` does not exist or is wrong as the process of matching has been massively based on the tag string. It has produced errors and also not everything has an item with definition in wikidata. What can be done to prevent this issue?
To get a good description for an item in the plugin, I am sometimes forced to create a reference in wikidata, which is very time consuming and my objective is too improve the SEO of my site, not fill wikidata with my brain juice. Gotcha ?

NOTE: Before coding, summarize in bullet points that you understand from the given instructions. Update the readme in the changelog in the readme and the version of the script when I validate the changes asked.







## PROMPT_10

I need a better UX for the plugin `Breadcrumb Migration Version 1.29.0`, through use, I discovered that the plugin needs improvements. Here are the changes needed that should take into account these observations.

1. In the tab "Bulk Description", I want to be able to export the selected tags meaning all the tags if it is the option that I chose or the set of selected ones the i should have 2 buttons that one export the data in CSV (button_3) and JSON (button_4). For the file breadcrumb_migration_bulk_description_[timesteamp].json or breadcrumb_migration_bulk_description_[timesteamp].csv

You have also to make a better UX with the existing buttons that must be at the same level as I will play with the same dataset. Capisce ?

1.1 Save Description to WordPress (button_2)
Copies Wikidata description → tag Description field for all selected rows.

1.2 ↺ Synchronize from WordPress (button_2)
What does this button actually do? Explain it briefly in the screen and more explicitly in the readme

1.3 so that a make line or a list with four buttons. Document also briefly button_3 and button_4 only in readme as it should be straightforwarded on the screen.

NOTE: Before coding, summarize in bullet points that you understand from the given instructions. Update the readme in the changelog in the readme and the version of the script when I validate the changes asked.







## PROMPT_9
I need a better UX for the plugin `Breadcrumb Migration Version 1.28.0`, through use, I discovered that the plugin needs improvements. Here are the changes needed that should take into account these observations.


1. In the tab "Bulk Description", for each tag,  the column `Wikidata ID` is often empty, as I have need tags coming constantly, so I need to perform a search on wikidata based the value `bm-desc-tag-name`, you can add a button `Search` at the right of the button `Fetch` so I can directly search on the string.
For instance, I have the label `chunking` and I should have the quickets way to grab the `Wikidata ID` that correpond to it on wikidata e.g `Chunking (Q5116438)`. Find the best way to do with the button `Search` that perform and may pouplate the `Wikidata ID` inside bm-desc-wikidata-id but also have a link on the right that launch the search in a target blank if I need to ensure that the correct `Wikidata ID` for the correct. Human valiadtion, it is called, capisce? 
`https://www.wikidata.org/w/index.php?search=chunking&language=en&title=Special%3ASearch&ns0=1`

 
NOTE: Before coding, summarize in bullet points that you understand from the given instructions. Update the readme in the changelog in the readme and the version of the script when I validate the changes asked.





## PROMPT_8

```text

Agile, AI development, AI ethics, AI ideology, AI philosophy, AI tools, AI workflow, Alex Karp, artificial intelligence, automation, cc-lens, CCTOP, chunking, Claude AI, Claude Code, Claude Code Token Optimization Problem, CLAUDE.md, cognitive tinkering, context handoff, cost reduction, digital product management, embeddings, FAISS, future of work, Gemini, HANDOFF.md, ingestion, large language model, liquid capitalism, LLM, mistral, open source, OpenWolf, Palantir, Perplexity, Product Owner, prompt engineering, python, RAG, Retrieval-Augmented Generation, semantic search, semantic SEO, session bridging, symbolic violence, technological progress, token limit, token management, token optimization, user stories, value-driven development, WordPress plugin


AI, breadcrumb, categories, Claude Code, Generative Engine Optimization, GEO, LLM, MCP, Model Context Protocol, named entities, negative externality, NLP, organic traffic, python, SEO, SERP, spacy, tags, Taxonomy, WebMCP, Wikidata, Wordpress, WordPress plugin




African languages, AI, AI agents, AI exploration, Amharic, Anthropic, augmented journalism, automation, bash, batch processing, breadcrumbs, business requirements, Claude AI, code-switching, containerization, content clustering, CSV structure, database migration, Deutsche Welle, digital sovereignty, digital transformation, Diola, DJO Project, Docker, Docker Compose, editorial workflow, embedding models, end-to-end process, fine-tuning, France Médias Monde, Fulfude, Gemini, GEO, GitHub, Hausa, Igbo, IPSI Tunisia, JSON format, Kirundi, Kiswahili, KPIs, large language models, ld+json, Lingala, LLM, low-resource languages, Mandenkan, Media Loves Tech, Mistral OCR, multilingualism, multimodal AI, MySQL, named entity recognition, Natural language processing, NER, NLP, OCR, Oromo, Perplexity, Peul, PhpMyadmin, plugin development, POC, post-processing, product discovery, proof of concept, python, related content, REST API, Schema.org, semantic clustering, semantic layer, semantic SEO, SEO, shell scripting, Somali, speech recognition, staging environment, structured output, Swahili, tag families, taxonomies, Tigrinya, transcription quality, Tunisian Arabic, user stories, vectorization, version control, Whisper, Wolof, Wordpress, Yoruba, Zulu



AI experiments in MLflow, AI from POC to scaling, AI industrialization with MLflow, AI JSON validation, generative AI control, improve LLM results, leveraging prompt engineering, LLM model configuration, LLM parameter tuning, LLM prompt engineering, MLflow and LLMs, MLflow features, MLflow for AI, MLflow integration, MLflow LLM management, Ollama AI integration, open-source LLMs, optimize LLM prompts, prompt quality enhancement, prompt tracking in MLflow, scaling AI projects, self-hosted LLMs, using MLflow with LLMs




#18DaysInEgypt, #idocs, 3WDOC, 3WDOC Studio, A navalla suiza, Brett Gaylor, Brian Chirls, Bristol, collusion, CSS3, digital citizenship, documentaire interactif, Eva Dominguez, Flash, Gerald Holubowicz, hecube, highrise, HTML5, i-doc, i-doc symposium, idoc, interactive documentary, Jigar Mehta, katerina cizek, María Yáñez, Mozilla Foundation, nfb, ONE MILLIONth TOWER, participation, Paulina Tervo, PopCorn JS, Popcorn Maker, prescription, rich-media, Sandra Gaudenzi, social media, Transmedia, University of West England, Web made movies, webdoc, Webdocumentaire, WebGL, Webmademovies, workshop, write this down





analyse, Canon, Philip Bloom, portrait, Sofia, technique, Webdocumentaire, analyse, codec, flv, mp3, technique, Thanatorama, Webdocumentaire, Contact, Formulaire, PHP, plugin, Wordpress



analyse, documentaire, Flash, flv, Intended Consequences, Jonathan Torgovnik, MediaStorm, technique

 
apache, CodeIgniter, Framework, Kohana, Linux, OOP, PHP, PHP5


actionscript, documentaire, Flash, Gaza, Israël Analyse, mov, Palestine, reportage, Sderot, technique


Adobe, apache, cloud computing, Ecology, Flash, Google, HTML5, Linux, PaaS, SaaS


.htpasswd, apache, Hébergement, Htaccess, Linux, mot de passe, protection répertoire
amour, Cyril Slucki, Ela & Dimitri, Lise Couzinier, temporalité, Transmedia, TransmediaLove



Agathe Films, Bruno Masi, Chechnya, Chernobyl, Cosaques, Crimea, documentaire, Gaité lyrique, Georgia, Guillaume Herbaut, Iran, La Montaña, La Zone, Lemonde.fr, livre, multimédia, Oeil Public, Ossetia, photographe, photojournaliste, Pripyat, Putin, ransmedia, révolution, russia, St Petersburg, Twitter, Webdocumentaire
```

## PROMPT_7
```text
Zeplin is a tool that helps you push ready-to-build designs, automate workflows, and build products faster. It connects design, development, and product teams across functions, lifecycles, and geographies.


YSlow is a tool that grades web pages based on Yahoo!'s rules for high performance web sites. It offers suggestions, statistics, and tools for improving the page's speed and efficiency across various browsers and platforms.
```

## PROMPT_6
```text
Wwwhatsnew

Wwwhatsnew.com is a technology media outlet founded in 2005 by Juan Diego Polo, a technology consultant with extensive experience in telecommunications engineering, IT project management, and web technology consulting.


Wwwhatsnew.com es un medio de tecnología fundado en 2005 por Juan Diego Polo, consultor tecnológico con una amplia trayectoria en ingeniería de telecomunicaciones, gestión de proyectos de TI y consultoría en tecnología web.

https://wwwhatsnew.com/
```

## PROMPT_5
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