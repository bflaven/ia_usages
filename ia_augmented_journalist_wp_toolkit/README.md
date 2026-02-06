# ia_augmented_journalist_wp_toolkit.md

**List of all the directories:**

- images_illustrations: illusration fr the main post
- prompt: directory with all the prompts.

## Introducing semantic clustering with IA in WordPress via a plugin

This workspace explores how to use text embeddings and semantic clustering to provide **related content** and smarter navigation inside WordPress.

- ia_wp_plugin_related_content_embedding_tags_semantic_clustering:  
  Core experimental plugin that computes embeddings for posts, pages, and taxonomy terms, then performs semantic clustering to build related-content groups and tag suggestions directly in WordPress.

- ia_wp_plugin_related_content_steps:  
  Helper plugin that exposes the full processing pipeline as sequential “steps” inside the WP admin (indexing content, generating embeddings, clustering, and writing relations back to post meta or custom tables) to make the workflow easier to debug and automate.

- ia_wp_plugin_tags:  
  Focused plugin dedicated to semantic tagging: it generates embeddings for content, compares them against a vectorized tag vocabulary, and proposes or auto-applies the most relevant tags to improve internal linking and SEO.

- wp_plugin_related_content_steps:  
  A leaner, WordPress‑only version of the step-based pipeline, designed to run even without external AI infrastructure, useful for testing UI flows, hooks, and data structures before connecting to real embedding backends.


## Introducing to mistral-ocr

These components demonstrate how to integrate Mistral OCR’s document-understanding capabilities into your AI workflows.

- ia_mistral_ocr:  
  Python/Node tooling and example scripts for calling the Mistral OCR API, extracting structured text from PDFs or images, and preparing the output (cleaned text, layout-aware blocks) for downstream tasks such as embeddings, search, or clustering.


## Introducing to Whisper (African languages, training)

This section focuses on adapting Whisper to under‑represented African languages and domain-specific speech data.

- ia_training_whisper:  
  Training and fine‑tuning environment for Whisper (datasets, configs, and scripts) targeting African languages, including utilities for data curation, LoRA/finetune experiments, and evaluation (WER, CER) to measure gains over base models.


## Introducing semantic clustering with the help of IA  into Wordpress via a plugin

- ia_wp_plugin_related_content_embedding_tags_semantic_clustering: 
- ia_wp_plugin_related_content_steps: 
- ia_wp_plugin_tags: 
- wp_plugin_related_content_steps: 



