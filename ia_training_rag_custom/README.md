# ia_training_rag_custom

## Intro (human made)
The initial goal was to create a chatbot using RAG and custom data from simple User Stories.

I targeted five markets likely to be interested: RFP (request for proposal), HR (human resources), screenwriting, and journalism.

The main core benefit is that RAG allows a human expert to navigate a dense corpus naturally, while maintaining a chain of traceability.

This project also provided the perfect opportunity for a true experiment with Claude Code, from design to final presentation, including complete development. A complete project, from start to finish, with no assistance other than Claude Code.

Consequently, a quick strategy was needed to safeguard the valuable Claude Code tokens so work could continue.

Furthermore, a RAG is great, but what other assets/products can be derived from the RAG product? Therefore, I repurposed part of the pipeline to create a semantic search based on the corpus of data used. To put it simply, imagine you're an HR Director. You have a Responsible Job Search Tool (RJS) that allows you to filter CVs using a search engine to determine if they match the job posting you've published. At the same time, you index all the CVs you receive using a semantic search. It's undoubtedly useful and not actually that complicated. Since I'm not an HR Director but a Product Owner (PO), I use it in my own articles and, with Claude Claude, I created a plugin to implement it on WordPress.

Then, finally, after completing all this work, I have been thinking more abstractly about the future of work in the age of AI.



## Intro (IA made)
This post is a personal and reflective essay by a Product Owner and AI Coordinator who uses Claude Code to build a RAG (Retrieval-Augmented Generation) application. The author weaves together two distinct threads: a practical account of building with Claude Code (including the painful discovery of token limits, the CLAUDE.md discipline, and tools like OpenWolf to manage token consumption), and a philosophical meditation on what AI means for human labor, identity, and society. The central practical insight is that Claude Code burns tokens voraciously if left unconstrained, and that a smart developer must treat tokens as a scarce resource — using other LLMs (Mistral, Perplexity) for documentation tasks and reserving Claude Code for thinking and coding. The philosophical thread questions whether AI augments or replaces human cognition, invokes Alex Karp's provocation about who survives the AI era, and critiques the ideology of individual empowerment that AI platforms sell — concluding that behind the optimism lies a logic of domination inherited from liberal capitalism.

**You can read the article on my blog**
[Claude Code, CLAUDE.md, and Token Optimization: Practical Tips for RAG Development Without Burning Your Credits](https://wp.me/p3Vuhl-3qO)


## editorial_simple_rag : 

The RAG's project for The RAG’s project for rfp (request for proposal) | hr (human ressource) | screenwriting | journalism.

```text
# US-001 — Procurement (RFP)
As a public procurement officer, I want to query tender documents using natural language to quickly identify relevant passages without reading each document in its entirety.

# US-002 — HR
As a recruitment officer, I want to query a corpus of resumes using natural language to find profiles matching a given criterion (skills, language, experience).

# US-003 — Writing / Documentary
As a screenwriter, I want to explore a thematic corpus (archives, notes, sources) using natural language to find connections between subjects, characters, or events.

# US-004 — Journalism / Investigation
As a journalist, I want to query a corpus of sensitive documents (e.g., the Epstein Files) using natural language to identify facts, names, dates, or connections relevant to my investigation.

# US-005 — Support
As a customer support agent, I want to query a corpus of tickets, FAQs, and internal knowledge using natural language, in order to quickly identify relevant answers and key snippets without rereading all the databases.
```

The 5 cases share:

	- A heterogeneous corpus of documents:
	- RFPs, CVs, scenario notes, survey documents, support tickets, KBs.
	- A natural language query.
	- The user does not construct a complex query, but asks a question in French/English.
	- A sourced and contextualized answer:
	- Structured answer + snippet + precise location within the source (section, title, page, ticket, etc.).

The design approach is clear:
RAG = enable a human expert to navigate a dense corpus naturally, while maintaining a chain of traceability.

## wp-rag-semantic-search:
How to leverage on the RAG just to grab a semantic searhc and imeplent it in WP.





