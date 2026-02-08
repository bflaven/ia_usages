# ia_augmented_journalist_wp_toolkit.md

The code below is extracted from this post from my blog:
AI-Augmented Journalism: Practical Implementation of Semantic Clustering, Multilingual Transcription, and WordPress Automation [https://wp.me/p3Vuhl-3q4](https://wp.me/p3Vuhl-3q4)




**List of all the directories:**

- images_illustrations: illusration fr the main post
- prompt: directory with all the prompts.
- wp_docker: Docker-based WordPress staging environment for testing the Semaphore plugin and related content clustering features.


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


## Audio version
I have made again an experiment with NotebookLM, using the post's content. So, here is this regular blog post "AI-Augmented Journalism: Practical Implementation of Semantic Clustering, Multilingual Transcription, and WordPress Automation" [https://wp.me/p3Vuhl-3q4](https://wp.me/p3Vuhl-3q4) converted into a podcast using NotebookLM.

- [AI-Augmented Journalism: Practical Implementation of Semantic Clustering, Multilingual Transcription, and WordPress Automation](https://on.soundcloud.com/AqNjInTzRbPoD7Hyv9)

**Summary made by NotebookLM**
```
This text reflects on the **critical intersection of artificial intelligence, digital sovereignty, and linguistic diversity**, specifically focusing on how global technology often neglects non-Western languages. The author explores the paradox of advocating for **responsible AI** while being dependent on major foreign models, emphasizing the importance of **cultural independence** through local model training. Practical technical projects are detailed, including **Whisper transcription experiments** for African languages like Wolof and Swahili, as well as the development of **WordPress plugins** for semantic clustering. The narrative highlights the phenomenon of **code-switching** in multilingual societies and the necessity of tailoring AI to recognize these complex speech patterns. Ultimately, the collection serves as both a **technical roadmap** and a philosophical argument for using AI to preserve **linguistic identity** and take control of one's digital destiny.
```






## Video
Coming soon

<!-- [text_XXX](https://www.youtube.com/watch?v=xxx)[![text_XXX](image_XXX.png)](https://www.youtube.com/watch?v=xxx) -->














