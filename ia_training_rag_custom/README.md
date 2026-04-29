# ia_training_rag_custom

## Intro
This post is a personal and reflective essay by a Product Owner and AI Coordinator who uses Claude Code to build a RAG (Retrieval-Augmented Generation) application. The author weaves together two distinct threads: a practical account of building with Claude Code (including the painful discovery of token limits, the CLAUDE.md discipline, and tools like OpenWolf to manage token consumption), and a philosophical meditation on what AI means for human labor, identity, and society. The central practical insight is that Claude Code burns tokens voraciously if left unconstrained, and that a smart developer must treat tokens as a scarce resource — using other LLMs (Mistral, Perplexity) for documentation tasks and reserving Claude Code for thinking and coding. The philosophical thread questions whether AI augments or replaces human cognition, invokes Alex Karp's provocation about who survives the AI era, and critiques the ideology of individual empowerment that AI platforms sell — concluding that behind the optimism lies a logic of domination inherited from liberal capitalism.

**You can read the article on my blog**
[Claude Code, CLAUDE.md, and Token Optimization: Practical Tips for RAG Development Without Burning Your Credits](https://wp.me/p3Vuhl-3qO)


## editorial_simple_rag : 

The RAG's project for Human Ressources, Screenwriting, Journalism / Investigative, Support Journalism.

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





