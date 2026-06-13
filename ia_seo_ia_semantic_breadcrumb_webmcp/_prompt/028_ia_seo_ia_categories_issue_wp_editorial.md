

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


- set_3
Change, Data consolidation, Data-centric approach,  Framing, Gold stages, News Topic Classification


- set_2
API, Bronze, Dataset, Deployment, FastAPI, GitHub directory, IA (Artificial Intelligence), LLM (Language Model), MLOps (Machine Learning Operations), Model Implementation, Modelling, NLP (Natural Language Processing), run, Sentiment Analysis, Silver, Streamlit, Vite.js, Webapp


- set_1
Change, Change management, Data consolidation, Data-centric approach, Design Thinking Process, Evaluation Strategy, Feature Engineering, Framing, Gold stages, Ideation, News Topic Classification, Prototype, Sprints, Time-to-market


- set_full
API, Bronze, Change, Change management, Data consolidation, Data-centric approach, Dataset, Deployment, Design Thinking Process, Evaluation Strategy, FastAPI, Feature Engineering, Framing, GitHub directory, Gold stages, IA (Artificial Intelligence), Ideation, LLM (Language Model), MLOps (Machine Learning Operations), Model Implementation, Modelling, News Topic Classification, NLP (Natural Language Processing), Prototype, run, Sentiment Analysis, Silver, Sprints, Streamlit, Time-to-market, Vite.js, Webapp



