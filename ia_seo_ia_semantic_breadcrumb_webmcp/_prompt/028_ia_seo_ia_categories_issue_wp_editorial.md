






## DEPOT_2

```text

digital autonomy, Product Owner


agentic browsers, Atlas, Comet, dbt, DuckDB, GDPR, Google Chrome, innovation theater, late-stage capitalism, natural search, OpenAI, organizational pathologies, personal data, privacy, surveillance



agentic browsers, AI, AI agents, AI exploration, Anthropic, artificial intelligence, Atlas, Comet, dbt, digital autonomy, digital sovereignty, digital transformation, DuckDB, GDPR, GEO, Google Chrome, innovation theater, late-stage capitalism, natural search, OpenAI, organizational pathologies, Perplexity, personal data, privacy, Product Owner, python, semantic layer, SEO, surveillance, taxonomies
```

```text
PANDAS PROFILING, Screaming Frog
Automate, Deploy, experimentation, P.O, pandas, POC, python, Screaming Frog, SEO, SQLite, Streamlit, visualization
```

```text
Collab, Dash, Jupyter Notebook, Panda, SQLite
```
```text
AI, artificial intelligence, CMS, coding, Collab, Dash, Deep Learning, experimentation, IA, Jupyter Notebook, language, Machine Learning, Natural language processing, neural networks, NLP, NTLK, numpy, P.O, Panda, python, SQLite, Streamlit, toolbox, visualization
```

## PROMPT_6
Give a wikidata definition in English for "Panda" (Q107387127) plus a set for "subclass of", "uses". Add also "aliases" with a pipe | separated list. Give an answer that eases the cut and paste of each element of the answer. No explanations just say the essential. Advise also how to add the official URL. Do not forget to remind the ID on wikidata for "subclass of" and "uses" e.g Subclass of: (P279), Uses: (P2283). In order to avoid duplicates, advice on a strategy to promote disambiguation is important. The description should clearly state something to distinguish it.

- source of definition
Pandas is a powerful Python library used for data manipulation and analysis, particularly suited for structured data. It simplifies tasks like loading, cleaning, and visualizing data, making it an essential tool for data analysis projects. 


The range of data visualization using Pandas. Whether you're a beginner at data visualization and analytics or you're already a proficient data scientist, this guide will help you reveal valuable information from the data by analyzing and visualizing data.

Print the result as plain text ```text...``` and not as a readme file by removing all tags like `**`, `##`, etc.

```text
Label:
pandas (Q107387127)

Aliases:
pandas | Python pandas | pandas library | pandas data analysis | pd (pandas)

Description:
Open-source Python software library for data manipulation, analysis and
visualization of structured and tabular data, providing DataFrame and Series
data structures with tools for loading, cleaning, transforming and exploring
datasets.

---

Subclass of (P279):
- software library (Q188860)
- data analysis software (Q1254596)
- free and open-source software (Q341)
- Python library (Q28865)

---

Uses (P2283):
- Python (Q28865)
- NumPy (Q543633)
- data visualization (Q6504722)
- data manipulation (Q) → may need to be created
- DataFrame (Q) → may need to be created
- Matplotlib (Q1970467)

---

Official website (P856):
https://pandas.pydata.org/

---

Disambiguation strategy:
- Item Q107387127 already exists — EDIT the existing item, do not create a new one.
- Navigate directly to:
  https://www.wikidata.org/wiki/Q107387127
- Verify the existing label, description and claims before adding anything
  to avoid redundant or conflicting statements.
- "pandas" (software) must be distinguished from giant panda (Q42738),
  red panda (Q181916), and Panda Security (Q3367831) — the existing
  description should clearly state "Python library for data analysis".
- Use lowercase "pandas" as canonical label, consistent with the
  official project branding.
- Add instance of (P31) → software library (Q188860) if not already present,
  alongside subclass of (P279) claims.
```


## PROMPT_5
Give a wikidata definition in English for "Plotly Dash" plus a set for "subclass of", "uses". Add also "aliases" with a pipe | separated list. Give an answer that eases the cut and paste of each element of the answer. No explanations just say the essential. Advise also how to add the official URL. Do not forget to remind the ID on wikidata for "subclass of" and "uses" e.g Subclass of: (P279), Uses: (P2283). In order to avoid duplicates, advice on a strategy to promote disambiguation is important. The description should clearly state something to distinguish it.

- source of definition
web analytic application framework. Dash is an open-source Python framework for creating interactive data visualization interfaces. It allows users to build web applications using only Python, making it accessible for those without advanced web development skills. 

Print the result as plain text ```text...``` and not as a readme file by removing all tags like `**`, `##`, etc.


```text
Label:
Plotly Dash

Aliases:
Dash | Dash by Plotly | Dash Framework | Python Dash | Dash Analytics Framework

Description:
Open-source Python web framework for building interactive data visualization and analytics web applications without requiring advanced front-end development skills, developed and maintained by Plotly.

---

Subclass of (P279):
- web application framework (Q1330336)
- data visualization software (Q3402533)
- free and open-source software (Q341)
- software framework (Q271668)

---

Uses (P2283):
- Python (Q28865)
- Plotly (Q7207507)
- React (Q19399674)
- Flask (Q460797)
- JavaScript (Q2005)
- data visualization (Q6504722)

---

Official website (P856):
https://dash.plotly.com/

---

Disambiguation strategy:
- Use label "Plotly Dash" not bare "Dash" to avoid collision with
  Dash cryptocurrency (Q15878970), Dash punctuation, or Dash (shell).
- Search before creating:
  https://www.wikidata.org/w/index.php?search=Plotly+Dash
- Add property developer (P178) with value Plotly Inc. to reinforce
  disambiguation against other "Dash" named software.
- In the description, always include "Python" and "Plotly" as the
  first disambiguating terms.
- Consider adding said-to-be-the-same-as (P460) pointing to
  Plotly (Q7207507) to clarify the relationship without merging.
```


## PROMPT_TPL
Give a wikidata definition in English for "XXX" plus a set for "subclass of", "uses". Add also "aliases" with a pipe | separated list. Give an answer that eases the cut and paste of each element of the answer. No explanations just say the essential. Advise also how to add the official URL. Do not forget to remind the ID on wikidata for "subclass of" and "uses" e.g Subclass of: (P279), Uses: (P2283). In order to avoid duplicates, advice on a strategy to promote disambiguation is important. The description should clearly state something to distinguish it.

- source of definition
XXX

Print the result as plain text ```text...``` and not as a readme file by removing all tags like `**`, `##`, etc.



## PROMPT_4
Same for "CodeceptJS is an open source testing framework that supports web, mobile, and API testing with various drivers and features."

## A_PROMPT_4

```text
Label:
CodeceptJS

Aliases:
CodeCept | CodeceptJS Framework | Codecept Testing Framework | CodeceptJS E2E

Description:
Open-source end-to-end testing framework supporting web, mobile and API
testing through multiple drivers, offering a human-readable BDD-style syntax
for writing automated test scenarios across different platforms and browsers.

---

Subclass of (P279):
- test automation framework (Q) → may need to be created
- software testing framework (Q7536896)
- free and open-source software (Q341)
- JavaScript library (Q783866)

---

Uses (P2283):
- JavaScript (Q2005)
- Node.js (Q908263)
- Selenium (Q1491001)
- Playwright (Q) → may need to be created
- WebDriver (Q17091645)
- behavior-driven development (Q1247015)
- API testing (Q) → may need to be created

---

Official website (P856):
https://codecept.io/

---

Disambiguation strategy:
- Use label "CodeceptJS" not "Codecept" to avoid collision with
  any generic "codecept" term.
- Add description qualifier "JavaScript testing framework" as first
  disambiguating term.
- Search before creating:
  https://www.wikidata.org/w/index.php?search=CodeceptJS
- Distinguish from Codeception (PHP testing framework, Q) by explicitly
  stating "JavaScript" and "Node.js" in the description and claims.
```





## PROMPT_3
Give a wikidata definition in English for "Epoch" plus a set for "subclass of", "uses". Add also "aliases" with a pipe | separated list. Give an answer that eases the cut and paste of each element of the answer. No explanations just say the essential. Advise also how to add the official URL. Do not forget to remind the ID on wikidata for "subclass of" and "uses" e.g Subclass of: (P279), Uses: (P2283). In order to avoid duplicates, advice on a strategy to promote disambiguation is important. The description should clearly state something to distinguish it.
- source of definition
Complete pass through the entire training dataset. A model is typically trained over multiple epochs.
Print the result as plain text ```text...``` and not as a readme file by removing all tags like `**`, `##`, etc.


## PROMPT_3
Give a wikidata definition in english for "Ludwig" plus a set for "subclass of", "uses". Add also "aliases" with a pipe | separated list. Give an answer that eases the cut and paste of each element of the answer. No explanations just say the essential. Advise also how to add the official URL. Do not forget to remind the ID on wikidata for "subclass of" and "uses" e.g Subclass of: (P279), Uses: (P2283).
- source of definition
Ludwig is a low-code framework for building custom AI models like LLMs and other deep neural networks.
Source : https://ludwig.ai/latest/

**Label:**
Ludwig

**Aliases:**
Ludwig AI | Ludwig Framework | Ludwig Low-Code AI | Uber Ludwig

**Description:**
Open-source low-code Python framework for building, training and deploying custom AI models including large language models and deep neural networks, without requiring extensive machine learning expertise.

---

**Subclass of (P279):**
- machine learning framework (Q107517065)
- software framework (Q271668)
- free and open-source software (Q341)

---

**Uses (P2283):**
- Python (Q28865)
- deep learning (Q197536)
- large language model (Q107520748)
- neural network (Q192776)
- AutoML (Q114633987)

---

**Official website (P856):**
`https://ludwig.ai/latest/`

---

**To add the official URL:**
On the Wikidata item page, add a statement with property **official website (P856)** and value `https://ludwig.ai/latest/`

> **Note:** Search `https://www.wikidata.org/w/index.php?search=Ludwig+AI` before creating a new item to avoid duplicates — "Ludwig" is a common name (composer, king) so disambiguation is important. The description should clearly state "AI framework" to distinguish it.

## PROMPT_3a
Give a wikidata definition in english for "NLTK" plus a set for "subclass of", "uses". Add also "aliases" with a pipe | separated list. Give an answer that eases the cut and paste of each element of the answer. No explanations just say the essential. Advise also how to add the official URL. Do not forget to remind the ID on wikidata for "subclass of" and "uses" e.g Subclass of: (P279), Uses: (P2283).
- source of definition
NLTK is a leading platform for building Python programs to work with human language data. It provides easy-to-use interfaces to over 50 corpora and lexical resources such as WordNet, along with a suite of text processing libraries for classification, tokenization, stemming, tagging, parsing, and semantic reasoning, wrappers for industrial-strength NLP libraries, and an active discussion forum.
Source : https://www.nltk.org/


**Label:**
NLTK

**Aliases:**
Natural Language Toolkit | NLTK Python | Python NLP Library | Natural Language Processing Toolkit

**Description:**
Open-source Python platform for building natural language processing programs, providing interfaces to corpora and lexical resources, text processing libraries for classification, tokenization, stemming, tagging, parsing and semantic reasoning.

---

**Subclass of (P279):**
- natural language processing toolkit (Q107520748)
- software library (Q188860)
- free and open-source software (Q341)

---

**Uses (P2283):**
- Python (Q28865)
- WordNet (Q223469)
- natural language processing (Q30642)
- tokenization (Q1070681)
- text corpus (Q1700246)

---

**Official website (P856):**
`https://www.nltk.org/`

---

**To add the official URL:**
On the Wikidata item page, add a statement with property **official website (P856)** and value `https://www.nltk.org/`

> **Note:** NLTK likely already has a Wikidata entry. Search `https://www.wikidata.org/w/index.php?search=NLTK` before creating a new item to avoid duplicates.



## PROMPT_2
Update the script `001_wikidata_api_add_item.py`. Fix the error and prevent the error when the item has been aleready been created.

```text
python 001_wikidata_api_add_item.py --sandbox
⚠ SANDBOX MODE — writing to test.wikidata.org
→ Loading item from: item_ntlk.yaml
ℹ Claims skipped automatically (test.wikidata.org lacks production properties)
✓ Logged in as Bruno Flaven@C767867msH87jsz*qjJ5HTRX
✓ CSRF token obtained
Traceback (most recent call last):
  File "/Users/brunoflaven/Documents/03_git/ia_usages/ia_seo_ia_semantic_breadcrumb_webmcp/wikidata_api_add_item/001_wikidata_api_add_item.py", line 421, in <module>
    main()
  File "/Users/brunoflaven/Documents/03_git/ia_usages/ia_seo_ia_semantic_breadcrumb_webmcp/wikidata_api_add_item/001_wikidata_api_add_item.py", line 411, in main
    new_qid = create_item(session, item_data, csrf_token, item["label_en"])
  File "/Users/brunoflaven/Documents/03_git/ia_usages/ia_seo_ia_semantic_breadcrumb_webmcp/wikidata_api_add_item/001_wikidata_api_add_item.py", line 332, in create_item
    raise RuntimeError(f"API error: {result['error']}")
RuntimeError: API error: {'code': 'modification-failed', 'info': 'Item [[Q246769|Q246769]] already has label "NLTK" associated with language code en, using the same description text.', 'messages': [{'name': 'wikibase-validator-label-with-description-conflict', 'parameters': ['NLTK', 'en', '[[Q246769|Q246769]]'], 'html': {'*': 'Item <a href="/wiki/Q246769" title="Q246769">Q246769</a> already has label "NLTK" associated with language code en, using the same description text.'}}], '*': 'See https://test.wikidata.org/w/api.php for API usage. Subscribe to the mediawiki-api-announce mailing list at &lt;https://lists.wikimedia.org/postorius/lists/mediawiki-api-announce.lists.wikimedia.org/&gt; for notice of API deprecations and breaking changes.'}
```

Note: Before coding, summarize in bullet points that you understand from the given instructions. Update the readme in the changelog in the readme and the version of the script when I validate the changes asked.

## PROMPT_1

Update the script `001_wikidata_api_add_item.py`
Take example on this new YAML `/data/item_ntlk.yaml` and generate a new template. Most of the time the `qid` are incorrect for `subclass_of` and `uses`. So I have a new example in the `/data/item_ntlk.yaml` template to replace the model `item_template.yaml`. You do not knwo the `qid` so we rather go for `label` only.


The command have sent is the following:
 
```text
python 001_wikidata_api_add_item.py --sandbox
```

Note: Before coding, summarize in bullet points that you understand from the given instructions. Update the readme in the changelog in the readme and the version of the script when I validate the changes asked.





## DEPOT

- set_2
Animation, Animoto, photos, Slideshow, Texte, vidéos


- set_1
RoR, Ruby on Rails, Webapplication



Animation, Animoto, AWS, Development, développement, Ezra Zygmuntowicz, GitHub, HAProxy, Lethal, Merb, photos, Phusion Passenger, RoR, Ruby on Rails, Slideshow, Texte, vidéos, Weapon, Webapp, Webapplication

- set_3
Change, Data consolidation, Data-centric approach,  Framing, Gold stages, News Topic Classification


- set_2
API, Bronze, Dataset, Deployment, FastAPI, GitHub directory, IA (Artificial Intelligence), LLM (Language Model), MLOps (Machine Learning Operations), Model Implementation, Modelling, NLP (Natural Language Processing), run, Sentiment Analysis, Silver, Streamlit, Vite.js, Webapp


- set_1
Change, Change management, Data consolidation, Data-centric approach, Design Thinking Process, Evaluation Strategy, Feature Engineering, Framing, Gold stages, Ideation, News Topic Classification, Prototype, Sprints, Time-to-market


- set_full
API, Bronze, Change, Change management, Data consolidation, Data-centric approach, Dataset, Deployment, Design Thinking Process, Evaluation Strategy, FastAPI, Feature Engineering, Framing, GitHub directory, Gold stages, IA (Artificial Intelligence), Ideation, LLM (Language Model), MLOps (Machine Learning Operations), Model Implementation, Modelling, News Topic Classification, NLP (Natural Language Processing), Prototype, run, Sentiment Analysis, Silver, Sprints, Streamlit, Time-to-market, Vite.js, Webapp



