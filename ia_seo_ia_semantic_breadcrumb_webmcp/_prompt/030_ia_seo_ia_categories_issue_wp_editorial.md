
- tags examples for LANGUAGE
```text
Mandenkan, Peul
andrew devigal, Andrew G King
```



## PROMPT_16
Fine with 1.25.0 changes. Do a better UX in 1.26.0. Update change log in readme. 

In the tab "Delta — New Tags", I need to improve the bulk action. Enable to define the Named entities from Spacy lists below in for all the tags selected. Make the UX easy to understand that is incorporated with the action "Add to migration" button. I am f.... sloth, u should know that.

```text
# Named entities from Spacy
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
PERCENT:     Percentage, including "%".
MONEY:       Monetary values, including unit.
QUANTITY:    Measurements, as of weight or distance.
ORDINAL:     "first", "second", etc.
CARDINAL:    Numerals that do not fall under another type.
```

## PROMPT_15

Fine with 1.24.0 changes. Do a better UX in 1.25.0. Update change log in readme. I have added a .gitignore for the sake of the plugin.

In the tab "Delta — New Tags", I need the bulk action. Select option, all tags select + button "Add to migration" that massively migrate the tags to the WP. I am f.... sloth, u should know that.

- tags examples
```text
5.x, 6.x, développement, Drupal, Module, MySQL, PHP, Tutorial
```
- url where the action takes place
```text
admin.php?page=breadcrumb-migration&tab=delta
```






## PROMPT_14

--- EVOLUTION_1 add to breadcrumb-migration in tab "Delta (plugin breadcrumb-migration)

In the tab "Delta — New Tags", add a texteare that authorize the cut and paste keywords list to import specific keywords list because I want to be able to grab specific tags. I can "Scan for new tags" on this list

```text
5.x, 6.x, développement, Drupal, Module, MySQL, PHP, Tutorial
```
```text
admin.php?page=breadcrumb-migration&tab=delta
```




```text
Name: Calabash
Name if disambiguation needed: Calabash (acceptance testing framework)
Description: Open source acceptance testing framework for writing and running automated UI acceptance tests on iOS and Android mobile applications.
Aliases: Calabash acceptance testing framework | Calabash mobile testing | Calabash iOS Android tests | Calabash test automation | Calabash-BDD

Instance of: software testing framework
Subclass of: acceptance testing framework (P279) | mobile application testing framework (P279) | open source software (P279)
Uses: automated UI testing (P2283) | behavior-driven development (P2283) | Cucumber framework (P2283) | Ruby language (P2283)

Source code repository: https://github.com/calabash/calabash-android
Source code repository property on Wikidata: source code repository (P1324)

Disambiguation strategy: keep description focused on mobile acceptance testing and use "Calabash (acceptance testing framework)" if risks confusion with other Calabash uses.

—

Name: Gherkin
Name if disambiguation needed: Gherkin (BDD language)
Description: Plain-text domain-specific language with structured keywords (Given/When/Then/And/But) for writing human-readable acceptance criteria and executable specifications in behavior-driven development.
Aliases: Gherkin language | Gherkin BDD language | Gherkin acceptance criteria | Gherkin DSL | Cucumber Gherkin

Instance of: programming language
Subclass of: domain-specific language (P279) | behavior-driven development language (P279) | specification language (P279)
Uses: acceptance criteria writing (P2283) | executable specifications (P2283) | Cucumber framework (P2283) | user stories (P2283) | test automation (P2283)

Official website: https://cucumber.io/docs/gherkin/
Official website property on Wikidata: official website (P856)

Disambiguation strategy: keep description focused on BDD language and structured syntax for acceptance criteria, and use "Gherkin (BDD language)" to distinguish from other uses.
```

```text
- Calabash
Calabash is an open source acceptance testing framework that allows you to write and run tests for iOS and Android applications.
https://github.com/calabash/calabash-android

- Gherkin
Gherkin is a set of keywords that give structure and meaning to acceptance tests written in plain language. Learn how to use Gherkin, localize it, and organize your step definitions with Cucumber.

At its core, Gherkin is a set of grammatical rules that enables users to write human-readable descriptions of software behaviors without delving into the technical details of their implementation.
```




```text

Calabash, Gherkin, Testing

Calabash
Calabash is an open source acceptance testing framework that allows you to write and run tests for iOS and Android applications.
https://github.com/calabash/calabash-android

Gherkin
Gherkin is a set of keywords that give structure and meaning to acceptance tests written in plain language. Learn how to use Gherkin, localize it, and organize your step definitions with Cucumber.

At its core, Gherkin is a set of grammatical rules that enables users to write human-readable descriptions of software behaviors without delving into the technical details of their implementation.




Android, Calabash, Gherkin, iOS, Mobile, Testing
```


## PROMPT_14
Give a wikidata definition in English for "Framer". Add something to the name specific to avoid ambiguity if needed plus a set for "subclass of", "uses". Add also "aliases" with a pipe | separated list. Give an answer that eases the cut and paste of each element of the answer. No explanations just say the essential. Advise also how to add the official URL. Do not forget to remind the ID on wikidata for "subclass of" and "uses" e.g Subclass of: (P279), Uses: (P2283). In order to avoid duplicates, advice on a strategy to promote disambiguation is important. The description should clearly state something to distinguish it.

- source of definition
Framer is the site builder trusted by leading startups and Fortune 500 companies. Build fast and scale more easily with an integrated CMS, analytics, localization, and SEO.
Framer:  Easily go from design to world-class site with Framer, the web builder for creative pros. Design and ship your dream site. Zero code, maximum speed. No-Code Website Builder · AI-Powered Design Tools · Free to Start


- official repo or official website
Add official website or official source code repository (P1324)
https://www.framer.com/


Add post or article e.g
https://flaven.fr/2017/07/framer-origami-prototyping-mobile-applications-with-the-best-ux-design-tool/


Print the result as plain text ```text...``` and not as a readme file by removing all tags like `**`, `##`, etc.




## A_PROMPT_14
```text
Name: Framer
Name if disambiguation needed: Framer (website builder)
Description: No-code website builder and design-to-site platform for creating, publishing, and scaling websites with CMS, analytics, localization, and SEO.
Aliases: Framer website builder | Framer web builder | Framer CMS | Framer no-code website builder | Framer design tool

Instance of: no-code development platform
Subclass of: website builder (P279) | content management system (P279) | design tool (P279)
Uses: website design (P2283) | content management (P2283) | search engine optimization (P2283) | localization (P2283) | web analytics (P2283)

Official website: https://www.framer.com/ 
Official website property on Wikidata: official website (P856)
Source code repository: if available, add with source code repository (P1324)

Disambiguation strategy: keep the description focused on the product category and main function, and use “Framer (website builder)” if the item risks confusion with the older prototyping tool or other uses.
```




## A_PROMPT_13
- for some other ressource
```text
Reference URL (P854) # official url

# retrieved # blog post title + url
Retrieved (P813) # date e.g 2026-06-15
Title (P1476) # title of the post
Reference URL (P854) # url of the post
```

## A_PROMPT_12
```text
if the source exists, you can publish it on Wikidata as a reference on the statement you are editing. Use Reference URL (P854) for a web page, and Retrieved (P813) for the access date; use Stated in (P248) only when the source itself has a Wikidata item. [upload.wikimedia](https://upload.wikimedia.org/wikipedia/commons/3/37/WikiSalon_Wikidata_Adding_References.pdf)

Copy-paste format:
Source URL: https://origami.design/documentation/index.html
Source URL: https://origami.design/tutorials/
Source URL: https://origami.design/
Source URL: https://flaven.fr/2017/07/framer-origami-prototyping-mobile-applications-with-the-best-ux-design-tool/

How to add it:
1. Open the statement on the Wikidata item.
2. Click add reference.
3. Choose reference URL (P854).
4. Paste the source URL.
5. Add retrieved (P813).
6. Publish. [upload.wikimedia](https://upload.wikimedia.org/wikipedia/commons/f/f2/WikiSalon_Wikidata_Editing_and_Enhancing_Entries.pdf)

For disambiguation, keep the description explicit enough to distinguish it from the paper-folding art: “free Mac design and prototyping tool created by Meta for interactive interface prototypes.” [origami](https://origami.design/documentation/index.html)

Official URL:
Add it as official website in the item, not as a reference. [wikidata](https://www.wikidata.org/wiki/Help:Sources)

Source code repository:
If you have the repo URL, add it with source code repository (P1324).

Suggested reference strategy to avoid duplicates:
- Use the most authoritative source first.
- Reuse the same reference URL for identical claims.
- Prefer one reference per statement unless you need multiple independent sources. [en.wikipedia](https://en.wikipedia.org/wiki/Wikipedia:How_to_add_sources_to_Wikidata)

```

## PROMPT_11
Give a wikidata definition in English for "Origami Studio" plus a set for "subclass of", "uses". Add also "aliases" with a pipe | separated list. Give an answer that eases the cut and paste of each element of the answer. No explanations just say the essential. Advise also how to add the official URL. Do not forget to remind the ID on wikidata for "subclass of" and "uses" e.g Subclass of: (P279), Uses: (P2283). In order to avoid duplicates, advice on a strategy to promote disambiguation is important. The description should clearly state something to distinguish it.

- source of definition
Origami
Get up to speed in Origami Studio. Learn how to build, preview and share your prototypes.

Origami Studio is a free design tool created by Meta and available for Mac. It allows designers to rapidly build and share interactive interfaces.


- personal repo
Add repo as source code repository (P1324)
https://origami.design/
https://origami.design/tutorials/


Add post or article e.g
https://flaven.fr/2017/07/framer-origami-prototyping-mobile-applications-with-the-best-ux-design-tool/


Print the result as plain text ```text...``` and not as a readme file by removing all tags like `**`, `##`, etc.



```
Label: Origami Studio
Description: Free Mac design and prototyping tool created by Meta for building, previewing, and sharing interactive interfaces.
Aliases: Origami | Origami Studio prototype tool | Origami design tool | Meta Origami

Instance of: software
Subclass of: interactive design software (P279) | prototyping software (P279)
Uses: user interface design (P2283) | interactive prototyping (P2283) | animation (P2283)
Source code repository: https://github.com/your-repo-origami-studio
Official URL: https://origami.design/ (add as official website on Wikidata)

Disambiguation strategy: keep the description specific with “free Mac design and prototyping tool created by Meta” and prefer aliases that do not match unrelated origami/craft topics.

Source references to use for the Wikidata edit:
- https://origami.design/documentation/index.html
- https://origami.design/tutorials/
- https://flaven.fr/2017/07/framer-origami-prototyping-mobile-applications-with-the-best-ux-design-tool/
```



## PROMPT_10

```text
Origami
Get up to speed in Origami Studio. Learn how to build, preview and share your prototypes.

Origami Studio is a free design tool created by Meta and available for Mac. It allows designers to rapidly build and share interactive interfaces.






- SET_DEDICATED_2
Framer, Mobile, origami, Quartz Composer

- SET_DEDICATED_1
DRY, MVP, wireframe, Workflow


- SET_MISSING_1
DRY, Framer, Mobile, MVP, origami, Quartz Composer, wireframe, Workflow


- SET_ALL
Agile, Android, API, Apple, DRY, Framer, iOS, Mobile, MVP, origami, POC, Quartz Composer, web, wireframe, Workflow

# Business & Case Studies
# https://flaven.fr/2017/07/framer-origami-prototyping-mobile-applications-with-the-best-ux-design-tool/


```

## PROMPT_9

```text
Anaconda, Computer Vision, Deep Learning, IA, Image Classification, json, JSON-SCHEMA, Models, Natural language processing, NTLK, Object Detection, P.O, python, TensorFlow Keras, Theano, Video Classification, Worpress
# AI & Machine Learning
# https://flaven.fr/2020/05/python-anaconda-worpress-json-json-schema-messy-post-with-few-practices-and-feedback-from-my-p-o-experience/



Creative, how-to, learning, Mind Mapping, practice, teaching, training
# Business & Case Studies
# https://flaven.fr/2020/05/mind-mapping-learn-better-and-be-more-creative-with-mind-mapping-a-small-introduction-to-mind-mapping/

```




## PROMPT_8

```text

--- 

Spike (Agile)


A Spike in Agile is a time-boxed research activity used to explore an idea, investigate a problem, or validate a technical approach before committing to development. The goal is learning, not delivering a working feature.

https://en.wikipedia.org/wiki/Spike_(software_development)

--- 

DAM (Digital Asset Management)
detox (homebrew)

articles, book chapters, definition, Diogenes, documentation, GitHub, markdown, Mauve, quotes, vocabulary, writing, Agile, Agile Toolkit, Apple, AppleScript, Automationn, Bulk, CI, Craft, DevOps, Docker, imagemagick, images, Lockdown, photoshop, processing, Scripts, scrum, solution, Spike

--- 


# SET_2
# Business & Case Studies
articles, book chapters, definition, Diogenes, documentation, GitHub, markdown, Mauve, quotes, vocabulary, writing



# SET_1
# Business & Case Studies
Agile, Agile Toolkit, Apple, AppleScript, Automationn, Bulk, CI, Craft, DevOps, Docker, imagemagick, images, Lockdown, photoshop, processing, Scripts, scrum, solution, Spike





# SET_2
console, documents, epub, generate document, html, markdown, md, pandoc, pdf, readme

# SET_1
AFP, DAM, detox, Digital Assets Management, exiftool, Getty, Homebrew, Image, metada, Metadata, photoshop, pictures, Reuters
```


## PROMPT_7
Give a wikidata definition in English for "detox (homebrew)" plus a set for "subclass of", "uses". Add also "aliases" with a pipe | separated list. Give an answer that eases the cut and paste of each element of the answer. No explanations just say the essential. Advise also how to add the official URL. Do not forget to remind the ID on wikidata for "subclass of" and "uses" e.g Subclass of: (P279), Uses: (P2283). In order to avoid duplicates, advice on a strategy to promote disambiguation is important. The description should clearly state something to distinguish it.

- source of definition
detox is a utility designed to clean up filenames. It replaces difficult to work with characters, such as spaces, with standard equivalents. It will also clean up filenames with UTF-8 or Latin-1 (or CP-1252) characters in them (i.e: foo bar – quz.avi -> foo_bar-quz.avi).

- personal repo
Add repo as source code repository (P1324)
https://github.com/dharple/detox
https://formulae.brew.sh/formula/detox
Add post or article e.g
https://flaven.fr/2019/07/image-metadata-dam-getting-metada-from-pictures/


Print the result as plain text ```text...``` and not as a readme file by removing all tags like `**`, `##`, etc.




## A_PROMPT_7


```text
Label:
detox (file renaming utility)

Aliases:
detox | detox CLI | detox homebrew | detox filename cleaner | detox Unix tool

Description:
Open-source Unix command-line utility for cleaning and sanitizing filenames
by replacing problematic characters such as spaces, UTF-8 and Latin-1
characters with standard safe equivalents.

---

Subclass of (P279):
- command-line software (Q189103)
- file manager (Q112032623)
- free and open-source software (Q341)
- Unix utility (Q754782)

---

Uses (P2283):
- UTF-8 (Q193907)
- Latin-1 (Q600830)
- regular expression (Q185359)
- Homebrew (Q2300846)
- C (Q15777)

---

Official website (P856):
https://formulae.brew.sh/formula/detox

Source code repository (P1324):
https://github.com/dharple/detox

Described at URL (P973):
https://flaven.fr/2019/07/image-metadata-dam-getting-metada-from-pictures/

---

Disambiguation strategy:
- Search before creating:
  https://www.wikidata.org/w/index.php?search=detox+file+utility
- Must be clearly distinguished from:
  detox (medical/drug withdrawal) → Q1198831
  Detox (rapper) → Q3023534
  Detox (Dr. Dre album) → Q846744
- Use label "detox (file renaming utility)" with parenthetical qualifier.
- Use different from (P1889) → Q1198831 to make medical disambiguation explicit.
- Add instance of (P31) → software (Q7397) as primary anchor claim.
- Include "Unix" and "filename" in description as first disambiguating terms.
- Add operating system (P306) → Unix (Q11368) or Linux (Q388)
  to further distinguish from non-technical uses of the word.
```








## PROMPT_6
Give a wikidata definition in English for "Sentence Embeddings" plus a set for "subclass of", "uses". Add also "aliases" with a pipe | separated list. Give an answer that eases the cut and paste of each element of the answer. No explanations just say the essential. Advise also how to add the official URL. Do not forget to remind the ID on wikidata for "subclass of" and "uses" e.g Subclass of: (P279), Uses: (P2283). In order to avoid duplicates, advice on a strategy to promote disambiguation is important. The description should clearly state something to distinguish it.

- source of definition
In natural language processing, a sentence embedding is a representation of a natural language text as a vector of numbers which encodes meaningful semantic information.

- personal repo
Add my repo https://github.com/bflaven/ia_usages as Add source code repository (P1324)

Print the result as plain text ```text...``` and not as a readme file by removing all tags like `**`, `##`, etc.

```text
Label:
Sentence Embedding

Aliases:
Sentence Embeddings | Sentence Vector | Text Embedding | Sentence Representation | Semantic Sentence Vector

Description:
Natural language processing technique representing a sentence as a dense
numeric vector encoding its semantic meaning, enabling mathematical
comparison of textual similarity and semantic search.

---

Subclass of (P279):
- word embedding (Q28777951)
- vector space model (Q1785087)
- natural language processing (Q30642)
- feature learning (Q) → may need to be created

---

Uses (P2283):
- natural language processing (Q30642)
- neural network (Q192776)
- cosine similarity (Q1083302)
- transformer (Q47533580)
- BERT (Q61631517)
- semantic similarity (Q) → may need to be created
- sentence-transformers (Q) → may need to be created

---

Official website (P856):
No single official URL — concept defined across multiple sources.
Use reference URL (P854):
https://en.wikipedia.org/wiki/Sentence_embedding

Source code repository (P1324):
https://github.com/bflaven/ia_usages

---

Disambiguation strategy:
- Search before creating:
  https://www.wikidata.org/w/index.php?search=sentence+embedding
- Must be distinguished from word embedding (Q28777951) — sentence
  embeddings encode full sentences, not individual tokens or words.
- Must be distinguished from document embedding and paragraph embedding —
  use description qualifier "sentence-level" as primary disambiguating term.
- Use different from (P1889) → word embedding (Q28777951) to make
  the distinction explicit.
- Use instance of (P31) → concept (Q151885) or
  natural language processing technique as anchor claim.
- Add named after (P138) → no single author; add significant person (P3342)
  → Jakob Uszkoreit or Nils Reimers if attribution is needed.
```



```text
- Content quality 
Content quality refers to how well content meets standards and best practices, such as accuracy, relevance, and accessibility. **High-quality content** is useful, reliable, and tailored to its audience, aligning with both brand goals and user needs.

- Sentence Embeddings
In natural language processing, a sentence embedding is a representation of a natural language text as a vector of numbers which encodes meaningful semantic information.
```

## A_ANSWER

Wikipedia has strict rules about self-promotion. Here is the honest picture:

```text
DIRECT ANSWER:
You cannot add your own GitHub repo as a Wikipedia article or link.
Wikipedia will delete it as self-promotion (WP:COI, WP:PROMO policies).

---

WHAT YOU CAN LEGITIMATELY DO:

1. WIKIDATA (most viable right now)
   Create items for tools hosted in your repo that have no QID yet:
   - PySentence-Similarity → new item
   - PyTextRank usage examples → contribute to existing PyTextRank item
   Add source code repository (P1324) pointing to your GitHub URL.
   This is factual, not promotional.

2. WIKIPEDIA EXISTING ARTICLES (indirect)
   If your repo contains a notable implementation or benchmark,
   add it as an external link or reference in an existing article:
   - spaCy article → https://en.wikipedia.org/wiki/SpaCy
   - Natural language processing article
   - TextRank article (if it exists)
   Only if your repo is genuinely cited or referenced elsewhere first.

3. BUILD NOTABILITY FIRST (prerequisite for Wikipedia)
   Wikipedia requires secondary sources independent of you:
   - Get your repo cited in a blog post, paper, or tutorial by others
   - Publish a companion article on flaven.fr and get it indexed
   - Get cited in spaCy community docs or awesome-nlp lists
   - Accumulate GitHub stars (signals independent interest)

4. GITHUB AWESOME LISTS (faster than Wikipedia)
   Submit a pull request to:
   - https://github.com/explosion/spaCy (community resources)
   - https://github.com/keon/awesome-nlp
   - https://github.com/brianspiering/awesome-dl4nlp
   These are indexed by Google and visible to practitioners.

5. WIKIDATA AS SEO ANCHOR
   Even without a Wikipedia article, a Wikidata item with:
   - instance of (P31) → software library
   - source code repository (P1324) → your GitHub URL
   - main subject (P921) → spaCy, NLP, sentence similarity
   ...gives your repo a structured semantic presence in the
   Linked Open Data cloud, visible to knowledge graph consumers.

---

REALISTIC PRIORITY ORDER:

Step 1 → Create Wikidata items for PySentence-Similarity and
          link to your repo via P1324.
Step 2 → Write about it on flaven.fr and LinkedIn (you already do this).
Step 3 → Submit to awesome-nlp lists.
Step 4 → Once cited externally, add as external link to spaCy Wikipedia page.
Step 5 → Only then consider a standalone Wikipedia article.
```


## PROMPT_6
Give a wikidata definition in English for "PyTextRank" plus a set for "subclass of", "uses". Add also "aliases" with a pipe | separated list. Give an answer that eases the cut and paste of each element of the answer. No explanations just say the essential. Advise also how to add the official URL. Do not forget to remind the ID on wikidata for "subclass of" and "uses" e.g Subclass of: (P279), Uses: (P2283). In order to avoid duplicates, advice on a strategy to promote disambiguation is important. The description should clearly state something to distinguish it.

- source of definition
PyTextRank is a Python library that implements the TextRank algorithm for extractive summarization and keyword extraction in natural language processing. It works as an extension of the spaCy library, allowing users to extract top-ranked phrases and infer links from unstructured text.

Print the result as plain text ```text...``` and not as a readme file by removing all tags like `**`, `##`, etc.


```text
Label:
PyTextRank

Aliases:
PyTextRank | Python TextRank | TextRank spaCy | spaCy TextRank | pytextrank

Description:
Open-source Python library implementing the TextRank algorithm as a spaCy
extension for extractive text summarization and keyword extraction from
unstructured natural language text.

---

Subclass of (P279):
- natural language processing tool (Q107520748)
- software library (Q188860)
- free and open-source software (Q341)

---

Uses (P2283):
- Python (Q28865)
- spaCy (Q28127706)
- TextRank (Q) → may need to be created
- natural language processing (Q30642)
- keyword extraction (Q) → may need to be created
- extractive summarization (Q) → may need to be created
- graph-based ranking (Q) → may need to be created

---

Official website (P856):
https://spacy.io/universe/project/spacy-pytextrank

Source code repository (P1324):
https://github.com/DerwenAI/pytextrank

---

Disambiguation strategy:
- Search before creating:
  https://www.wikidata.org/w/index.php?search=PyTextRank
- No known QID exists yet — safe to create a new item.
- Must be distinguished from raw TextRank algorithm (academic paper,
  Mihalcea & Tarau 2004) — PyTextRank is the Python implementation,
  not the original algorithm.
- Use instance of (P31) → software library (Q188860) as anchor claim.
- Add based on (P144) → TextRank if a TextRank QID exists or is created,
  to explicitly link implementation to source algorithm.
- Include "spaCy extension" in description as primary disambiguating term
  against other TextRank implementations.
```


## PROMPT_5
Give a wikidata definition in English for "PySentence-Similarity" plus a set for "subclass of", "uses". Add also "aliases" with a pipe | separated list. Give an answer that eases the cut and paste of each element of the answer. No explanations just say the essential. Advise also how to add the official URL. Do not forget to remind the ID on wikidata for "subclass of" and "uses" e.g Subclass of: (P279), Uses: (P2283). In order to avoid duplicates, advice on a strategy to promote disambiguation is important. The description should clearly state something to distinguish it.

- source of definition
PySentence-Similarity is a tool designed to identify and find similarities between sentences and a base sentence, expressed as a percentage

Print the result as plain text ```text...``` and not as a readme file by removing all tags like `**`, `##`, etc.


```text
Label:
PySentence-Similarity

Aliases:
PySentence Similarity | Sentence Similarity Python | Python Sentence Matcher | PySentenceSimilarity

Description:
Open-source Python tool for computing and ranking similarity between sentences
and a base sentence, returning results expressed as a percentage score.

---

Subclass of (P279):
- natural language processing tool (Q107520748)
- software library (Q188860)
- free and open-source software (Q341)

---

Uses (P2283):
- Python (Q28865)
- natural language processing (Q30642)
- semantic similarity (Q) → may need to be created
- sentence embedding (Q) → may need to be created
- cosine similarity (Q1083302)

---

Official website (P856):
https://github.com/goldpulpy/pysentence-similarity
https://github.com/bflaven/ia_usages/tree/main/ia_using_spacy
→ add reference URL (P854) if no dedicated domain exists

---

Disambiguation strategy:
- Search before creating:
  https://www.wikidata.org/w/index.php?search=PySentence-Similarity
- No known QID exists yet — safe to create a new item.
- Description must include "Python" and "percentage score" as primary
  disambiguating terms against other sentence similarity tools
  (e.g. sentence-transformers, SimCSE, BERTScore).
- Use instance of (P31) → software (Q7397) as anchor claim.
- If hosted solely on GitHub, use source code repository (P1324)
  → https://github.com/bflaven/ia_usages as the primary URL claim
  instead of or alongside official website (P856).
```


```text

- pysentence-similarity
PySentence-Similarity is a tool designed to identify and find similarities between sentences and a base sentence, expressed as a percentage

- pytextrank
PyTextRank is a Python library that implements the TextRank algorithm for extractive summarization and keyword extraction in natural language processing. It works as an extension of the spaCy library, allowing users to extract top-ranked phrases and infer links from unstructured text.

- Content quality 
Content quality refers to how well content meets standards and best practices, such as accuracy, relevance, and accessibility. **High-quality content** is useful, reliable, and tailored to its audience, aligning with both brand goals and user needs.

- Sentence Embeddings
In natural language processing, a sentence embedding is a representation of a natural language text as a vector of numbers which encodes meaningful semantic information.



--- set_1
AI-Generated Text, Content Quality, Correctness, Downsides, Environment, Hallucinations, Labor Market, pysentence-similarity, pytextrank, Sentence Embeddings, spacy-llm, Usefulness, Validation







--- all
AI, AI-Generated Text, artificial intelligence, Content Quality, Correctness, Downsides, Environment, Hallucinations, Labor Market, pysentence-similarity, pytextrank, Sentence Embeddings, spacy-llm, Usefulness, Validation
```



```text
agentic browsers, dbt, digital autonomy, DuckDB, innovation theater, natural search, organizational pathologies, privacy
```

## PROMPT_4
Give a wikidata definition in English for "DuckDB" (Q133271766) plus a set for "subclass of", "uses". Add also "aliases" with a pipe | separated list. Give an answer that eases the cut and paste of each element of the answer. No explanations just say the essential. Advise also how to add the official URL. Do not forget to remind the ID on wikidata for "subclass of" and "uses" e.g Subclass of: (P279), Uses: (P2283). In order to avoid duplicates, advice on a strategy to promote disambiguation is important. The description should clearly state something to distinguish it.

- source of definition
DuckDB is an open-source column-oriented Relational Database Management System (RDBMS). It is designed to provide high performance on complex queries against large databases in embedded configuration, such as combining tables with hundreds of columns and billions of rows. Unlike other embedded databases (for example, SQLite) DuckDB is not focusing on transactional (OLTP) applications and instead is specialized for online analytical processing (OLAP) workloads.[3] The project has over 6 million downloads per month.

Print the result as plain text ```text...``` and not as a readme file by removing all tags like `**`, `##`, etc.



```text
Label:
DuckDB (Q133271766)

Aliases:
DuckDB | Duck DB | DuckDB OLAP | DuckDB Analytics | In-process SQL OLAP

Description:
Open-source in-process column-oriented RDBMS specialized for OLAP workloads.

---

Subclass of (P279):
- relational database management system (Q172757)
- column-oriented DBMS (Q1500328)
- free and open-source software (Q341)
- embedded database (Q1047234)

---

Uses (P2283):
- SQL (Q47607)
- online analytical processing (Q901407)
- Apache Arrow (Q116682975)
- Python (Q28865)
- R (Q206904)

---

File format (P2701):
- Parquet (Q99588765)
- CSV (Q935809)
- JSON (Q2063663)
- Apache Arrow (Q116682975)
- DuckDB file (.db) → may need to be created

---

Official website (P856):
https://duckdb.org/

---

Disambiguation strategy:
- Item Q133271766 already exists — EDIT, do not create a new one.
- Navigate to: https://www.wikidata.org/wiki/Q133271766
- Use different from (P1889) → SQLite (Q319417) to explicitly
  distinguish OLAP (DuckDB) from OLTP (SQLite).

-----------------
Label:
DuckDB (Q133271766)

Aliases:
DuckDB | Duck DB | DuckDB OLAP | DuckDB Analytics | In-process SQL OLAP

Description:
Open-source in-process column-oriented relational database management system
specialized for online analytical processing (OLAP) workloads, designed for
high performance on complex queries against large datasets in embedded
configuration, distinct from transactional (OLTP) databases such as SQLite.

---

Subclass of (P279):
- relational database management system (Q172757)
- column-oriented DBMS (Q1500328)
- free and open-source software (Q341)
- embedded database (Q1047234)

---

Uses (P2283):
- SQL (Q47607)
- online analytical processing (Q901407)
- Apache Arrow (Q116682975)
- Python (Q28865)
- R (Q206904)

---

Official website (P856):
https://duckdb.org/

---

Disambiguation strategy:
- Item Q133271766 already exists — EDIT the existing item, do not create a new one.
- Navigate directly to:
  https://www.wikidata.org/wiki/Q133271766
- Verify existing label, description and claims before adding anything
  to avoid redundant or conflicting statements.
- "DuckDB" must be distinguished from SQLite (Q319417) and other
  embedded databases — description must explicitly state "OLAP" and
  "column-oriented" as primary disambiguating terms.
- Add instance of (P31) → software (Q7397) and
  relational database management system (Q172757) if not already present.
- Avoid merging or linking with SQLite (Q319417) — they are distinct:
  DuckDB is OLAP-focused, SQLite is OLTP-focused.
  Use different from (P1889) → SQLite (Q319417) to make this explicit.
```


## DEPOT
agentic browsers, dbt, digital autonomy, DuckDB, innovation theater, natural search, organizational pathologies, privacy


## A_PROMPT_3
there is no related to I found has list is that OK ?


Yes, perfectly fine. Here is the corrected mapping using **has list (P2354)**:

```text
REVISED PROPERTY CHOICE:

If "has list" (P2354) is what Wikidata proposes in autocomplete,
it is NOT the right property for this use case.

---

BETTER ALTERNATIVES to "related to (P2579)"
(use whichever autocomplete finds first):

For privacy and GDPR:
  main subject (P921)
  → use when the concept is a core topic of the item

For OpenAI:
  developer (P178)
  → use if OpenAI built or maintains the agentic browser
  or
  maintained by (P126)

For Atlas and Comet:
  has part or parts (P527)
  → use if Atlas/Comet are components or variants
  or
  different from (P1889)
  → use to distinguish Q135456040 from Atlas/Comet if they are separate items

For all five concepts as general associations:
  topic's main category (P910)
  or
  keywords: use description field + aliases instead of a property,
  if no clean property fits.

---

PRACTICAL ADVICE:

In the Wikidata search box for properties, try typing:
  "main subject"   → P921  (most flexible, widely accepted)
  "developer"      → P178
  "has part"       → P527
  "different from" → P1889

P921 (main subject) is your safest fallback for
privacy, GDPR, OpenAI, Atlas, and Comet when no
more specific property fits.
```



## PROMPT_2
I want to relate on wikipedai `agentic browsers` to the other cooncepts `privacy, OpenAI, Atlas, Comet, GDPR` how do I do ?
```text
--- agentic browsers -> https://www.wikidata.org/wiki/Q135456040. Need link to privacy, OpenAI, Atlas, Comet, GDPR.
```

```text
EXISTING ITEM:
Agentic browser (Q135456040)
https://www.wikidata.org/wiki/Q135456040

---

STRATEGY: Add statements (claims) to Q135456040 linking to related concepts.

---

RELATED CONCEPTS — recommended properties and QIDs:

Privacy
  Property: related to (P2579) or significant topic (P7867)
  QID: privacy (Q8060)
  URL: https://www.wikidata.org/wiki/Q8060

GDPR
  Property: related to (P2579) or subject has role (P2868)
  QID: General Data Protection Regulation (Q1190952)
  URL: https://www.wikidata.org/wiki/Q1190952

OpenAI
  Property: developer (P178) or related to (P2579)
  QID: OpenAI (Q21980377)
  URL: https://www.wikidata.org/wiki/Q21980377

Atlas (browser agent by OpenAI)
  Property: related to (P2579) or said-to-be-the-same-as (P460)
  QID: → search first: https://www.wikidata.org/w/index.php?search=Atlas+OpenAI+browser
  May need to be created if no QID exists yet.

Comet (browser agent)
  Property: related to (P2579)
  QID: → search first: https://www.wikidata.org/w/index.php?search=Comet+agentic+browser
  May need to be created if no QID exists yet.

---

HOW TO ADD EACH LINK (manual):

1. Go to https://www.wikidata.org/wiki/Q135456040
2. Click "Add statement"
3. Enter the property (e.g. P2579 for "related to")
4. Enter the target QID (e.g. Q8060 for privacy)
5. Save — repeat for each concept.

---

BEST PROPERTY CHOICES SUMMARY:

related to            (P2579)  → privacy, GDPR, Atlas, Comet
developer             (P178)   → OpenAI (if OpenAI developed the item)
uses                  (P2283)  → OpenAI API if technically used
has part or parts     (P527)   → Atlas, Comet if they are sub-components
said-to-be-the-same-as (P460) → only if Atlas or Comet overlap with Q135456040

---

DISAMBIGUATION NOTE:
"Comet" and "Atlas" are common names — search Wikidata carefully before
creating new items or linking, to avoid connecting to unrelated QIDs
(e.g. Comet the spacecraft, Atlas the mythology figure).
```
Atlas
https://www.wikidata.org/wiki/Q136549314
Comet
https://www.wikidata.org/wiki/Q135264718



## PROMPT_1

- CREATE 
```text
- *** dbt -> dbt turns data work into a shared, scalable practice by bringing the best of software engineering to the analytics workflow. https://www.getdbt.com/product/what-is-dbt

dbt (data build tool) is an **open-source analytics engineering framework** that transforms raw data into analysis-ready datasets using SQL, enabling teams to write modular, version-controlled workflows that are easy to test and document. This approach helps bridge the gap between data analysts and engineers, making data work more collaborative and efficient.


- *** natural search -> natural language search -> ???

- *** digital autonomy -> ??? https://www.wikidata.org/wiki/Q104739680

- *** innovation theater -> ???

- *** organizational pathologies -> ???
```
- UPDATE
```text
--- agentic browsers -> https://www.wikidata.org/wiki/Q135456040. Need link to privacy, OpenAI, Atlas, Comet, GDPR.
```

- DONE
```text
--- AI exploration -> https://www.wikidata.org/wiki/Q11660
--- privacy -> https://www.wikidata.org/wiki/Q188728
--- DuckDB -> https://www.wikidata.org/wiki/Q111343643
--- OpenAI -> https://www.wikidata.org/wiki/Q21708200
--- Atlas -> Atlas browser -> https://www.wikidata.org/wiki/Q136549314
--- Comet -> Comet browser ->  https://www.wikidata.org/wiki/Q135264718
```


## DEPOT_VALIDATION_3

```text
agentic browsers, AI exploration, Atlas, Comet, dbt, digital autonomy, DuckDB, innovation theater, natural search, OpenAI, organizational pathologies, privacy
```

## PROMPT_TPL
Give a wikidata definition in English for "XXX" plus a set for "subclass of", "uses". Add also "aliases" with a pipe | separated list. Give an answer that eases the cut and paste of each element of the answer. No explanations just say the essential. Advise also how to add the official URL. Do not forget to remind the ID on wikidata for "subclass of" and "uses" e.g Subclass of: (P279), Uses: (P2283). In order to avoid duplicates, advice on a strategy to promote disambiguation is important. The description should clearly state something to distinguish it.

- source of definition
XXX

Print the result as plain text ```text...``` and not as a readme file by removing all tags like `**`, `##`, etc.


