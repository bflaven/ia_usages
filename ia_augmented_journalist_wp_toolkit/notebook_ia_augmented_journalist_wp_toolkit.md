# Reflections on Digital Silence, AI, and Language Sovereignty

It's been ages since I've written anything or posted a video on YouTube. My online presence is abysmal. Is this the beginning of the wisdom of keeping quiet when you have nothing to say, or is it merely another manifestation of what I call **Digital January Diet (DJD)**?

This raises a fundamental question: Why blame myself and see this prolonged absence as a disadvantage? Isn't it said that distance creates power? Why not approach the problem from the opposite angle and finally celebrate frugality in a society of abundance—where everyone feels compelled to have something to say about everything, including AI?

> **For this post**, you can find all files and prompts on my GitHub account: [ia_augmented_journalist_wp_toolkit](https://github.com/bflaven/ia_usages/tree/main/ia_augmented_journalist_wp_toolkit)

---

## The Virtue of Restraint

Can't we opt for a more reasonable and virtuous counterpoint? Consider these opposing forces:
- Gluttony vs. Frugality
- Debauchery vs. Abstinence
- Lies vs. Truth
- Dependence vs. Sovereignty
- ...the list goes on

I'll let you guess where I stand between these rather black-and-white positions.

---

## The Paradox I Embody

My characteristic mild cynicism tells me that claiming to be on one side or the other is just posturing. I know this all too well: I advocate for the responsible use of AI yet abuse it whenever possible. I express concern about LLM sovereignty while using American or Chinese models all day long. The contradictions are glaring.

---

## The Backlog

I mainly want to wrap up some topics I've been working on so I can move forward. My Mac is overflowing with Proofs of Concept (POCs), trial-and-error experiments, and unfinished projects. There's been a lull in my publishing schedule—much like when dishes pile up in the sink or laundry accumulates, and you finally have to deal with it.

Specifically, I'm exploring technical AI topics for personal projects, inventing and creating while earning a salary for doing very little—or at least avoiding the most challenging work.

---

## The Fear of Imperfection

I'm still hesitant to publish all my trial-and-error work: the adjustments, the sometimes botched workarounds, the risky guesswork, or simply anything that reveals my ignorance. Yet recognizing one's ignorance is the first step in learning.

---

## AI's Revolutionary Impact

It must be acknowledged that AI is sweeping everything away: posture, knowledge, hierarchical functions—literally everything. Nothing seems to resist it: not advice, not training, not technical skills. It's reminiscent of the French revolutionary slogan of 1789: "Liberty or death"—except now it's **"AI or death."**

---

## Publishing Prompts: A Record of Cognitive Process

My approach moving forward is to publish all my prompts. They serve as a record of my cognitive process—"step by step," or perhaps more accurately, "error by error."

By publishing my prompts, you'll also see that I'm increasingly suffering from intellectual laziness, especially when it comes to writing code. I would be utterly unable to produce even a quarter of what I now create without AI assistance, including presentations.

> **For transparency:** This code was primarily written by Claude and Perplexity.

---

# Words Have Meaning

## Why Transcription Quality Matters for Underserved Languages

Why did I become interested in the quality of transcriptions on Whisper and the problem of "neglected" languages, particularly Arabic and African languages?

The answer is professional necessity. I manage content in several of these languages, and not everyone is going to end up speaking English. Technological dominance is one thing; cultural dominance is another entirely.

---

## Languages and Collaborations

Professionally, I work with the following languages: **Mandinka, Fulfulde, Hausa, and Swahili.**

Thanks to **Codou Ndiaye** and the creators of the **DJO project**—Fares Mallouli and Mohamed Amine Macherki, winners of the Deutsche Welle MEDIA LOVES TECH Grand Prize—I also became interested in **Wolof** and **Tunisian Arabic**.

- [DJO Project](https://akademie.dw.com/en/an-ai-platform-wins-top-2025-media-loves-tech-prize/a-75134414)

I have collaborated with Codou Ndiaye on two subjects:
- Using AI for Wolof
- Conducting experiments with AI for customer support

With the DJO founders, I discussed their project for automatic transcription of the Tunisian dialect, exploring the challenges of multilingialism, data collection, and the technical specificities related to **code-switching**.

---

## Understanding Code-Switching

DJO trained Whisper to improve its transcription performance for the three languages that comprise Tunisian Arabic: **English, French, and the Tunisian dialect**. According to Codou Ndiaye, the same operation should be carried out in Senegal, but with an even larger number of language combinations. Multilingualism is far more widespread in Africa, and its corollary—**code-switching**—is a critical factor.

> **Code-switching** is the alternation between several linguistic codes (languages, dialects, or language registers) within a single discourse or utterance, or even within a sentence, most often where the syntax of the two codes aligns.
> — [Wikipedia](https://en.wikipedia.org/wiki/Code-switching)

### Common Code-Switching Patterns in Senegal
- English, French, and Wolof
- English, French, and Diola
- English, French, and Fulfulde (Peul)

Understanding and accommodating code-switching is a prerequisite for offering transcription services to journalists or customer support chatbots in countries like Senegal or Tunisia.

---

## Digital Sovereignty and Independence

Building models specifically trained for local markets and their speakers is a mark of sovereignty and digital independence. This is not merely a technical consideration—it's a political and cultural imperative.

### The GAFA Gap
The eagerness of major tech companies (Meta, OpenAI, Google, Anthropic, Amazon, Apple, etc.)—mostly American and therefore English-speaking—to invest in these languages is undoubtedly quite limited. Multiple factors contribute:
- Lack of language resources to train models
- Lack of available speakers to correct inferences
- Questionable financial returns proportional to investment
- Increasingly aggressive American diplomacy

Meanwhile, Africa is the object of intense interest from three major powers: the USA, Russia, and China. Offering models adapted to local languages could provide a significant soft power advantage to whichever nation takes the initiative.

---

## The Power of Language

Language is, after all, the essential vehicle for many things: culture, discourse, politics, information. Words have meaning, and their precision in transcription is paramount.

> **"The limits of my language are the limits of my world."** — Ludwig Wittgenstein

---

## Market Dynamics and Self-Determination

The danger of disintermediation, combined with cultural and technological dominance, lies in the fact that fragmented demand weakens you as an individual or group of individuals in the face of supply that naturally tends to concentrate.

Thus, if you represent a small fraction of humanity—for example, if you speak a rare language or belong to a minority linguistic community—there is little chance you will be served well, or perhaps not served at all, because you represent a negligible market share. This is the harsh reality of the market.

What remains is to take control of your destiny by training your own LLM (Large Language Model) and thus seizing power and sovereignty. This is the driving force behind my practice.

---

# From Theory to Implementation

## 1. Testing Transcription on Specific Languages with Whisper

I wanted to evaluate Whisper's ability to transcribe audio and video in specific languages, with the goal of either finding pre-trained Whisper models for these languages or training Whisper myself. This is primarily product discovery: checking the capability of existing standard market models to handle languages beyond European ones (English, Spanish, French) and test performance on languages like **Brazilian Portuguese, Chinese, Hausa, Kiswahili, Vietnamese, and Wolof**.

---

## 2. Testing Mistral OCR

Handling heterogeneous files and formats requires choosing a high-performance and versatile OCR model. This is the promise of **Mistral OCR**, which I wanted to test.

### Why Mistral OCR?
- State-of-the-art understanding of complex documents
- Natively multilingual and multimodal
- Doc-as-prompt, structured output
- Selectively available to self-host for organizations dealing with highly sensitive or classified information

- [Mistral OCR Documentation](https://mistral.ai/news/mistral-ocr)

---

## 3. Testing Related Content: Semantic Clustering for WordPress

### The Challenge: From Traditional SEO to Semantic SEO

My question is: How do we manage the transition from traditional SEO to meaning-based SEO built around semantic clusters, where tags respond to each other and form semantic pools interpretable by AI bots? This helps us better understand the logic of **GEO (Generative Engine Optimization)**.

### Editorial Workflow Control

I decided to apply this semantic clustering transformation to my own blog.

### The WordPress Plugin Development

I attempted to create a WordPress plugin—to master the end-to-end editorial workflow, from template management and keyword cleaning (sometimes across multiple languages) to named entity recognition and integration into a CMS.

- [WordPress Categories and Tags: Powerful SEO Tips To Practice](https://www.wpdownloadmanager.com/wordpress-categories-and-tags-seo/)

### Personal Roadmap
```
+ TODO: Plugin for AI-suggested tags using named entities
+ TODO: Plugin for AI-suggested categories for category selection
+ TODO: Plugin for AI-suggested pictures for default images
```

### Operating Procedure for Related Posts
```
# POINT_1: Decide what to vectorize per post (DONE, 003_parsing_posts_vectorize_per_post.py)
# POINT_2: Choose and configure an embedding model (DONE, 004_parsing_posts_choose_embedding_model.py)
# POINT_3: Design a small vectorization API (TODO, 005_parsing_posts_vectorization_api.py)
# POINT_4: Implement pre-processing + batching (TODO)
# POINT_5: Plan for reproducibility and configuration (TODO)
# POINT_6: Connect STEP_1 to later steps (high level) (TODO)
```

### Project Directories
- ia_wp_plugin_related_content_embedding_tags_semantic_clustering
- ia_wp_plugin_related_content_steps
- ia_wp_plugin_tags
- wp_plugin_related_content_steps

---

## Understanding Semantic Clustering

I asked several AI systems (Perplexity, Claude, Gemini) about semantic clustering. Here is a short digest.

> **NOTE:** Always be wary of the laudatory tone of AI responses.

### Synthesis on Semantic Clustering
The approach on Semantic Clustering is not only valid but forward-thinking. It correctly anticipates the SEO to GEO transition by creating a semantic clustering infrastructure that:
- Maintains classic SEO compatibility
- Prepares the groundwork for GEO
- Facilitates migration from flat taxonomies to organic multilingual hierarchies
- Preserves human editorial validation

---

## Information Risks in the Media Economic Model

I asked about information risks due to the collapse of the media economic model. This led deeper into a nightmare scenario based on:
- Paradox of ephemeral abundance
- Temporal compression effect of information
- Instant obsolescence syndrome
- Speed vs. truthfulness dilemma

All of these lead to: **(1) Speed Over Quality, (2) Fragmentation and Ephemerality, (3) Attention Economy!**

---

## Look & Feel: AI Output in the WordPress Theme

We all know that any functionality, even AI-powered, can fail if the UX and look-and-feel are poor. So I've reworked the output for both the breadcrumb and sidebar from the code output in the WordPress theme.

---

## Using Docker to Test WordPress and the Plugin

```
# Commands for DOCKER

# Go to path
cd /Users/brunoflaven/Documents/01_work/blog_articles/_ia_augmented_journalist_wp_toolkit/ia_wp_plugin_related_content_steps/wp_docker

# Up docker
docker compose up -d

# Down docker
docker compose down
```

---

## Testing More Advanced Features (ENABLE LEVEL_2)

Creating a detailed plugin assessment involves describing the exact procedure of what you want to achieve as objectives in terms of business value, then assigning KPIs to reach these results.

> **Example:**
> - **As a business requirement:** The plugin assessment should include clear business objectives and KPIs. For example, increase the audience for technical tags (Python, Docker, AI) by 15% in English-speaking countries (USA, India) within 6 months, measured by unique page views.
> - **As a user story:** As a content strategist, I want to use [plugin/tool] to increase the audience for technical tags (Python, Docker, AI) by 15% in English-speaking countries (USA, India) within 6 months, so that we can grow our international user base.

---

## Technical Validation Documentation

```
# HOW_TO_1: Validate ld+json in code
- In post page source, look for script type="application/ld+json" and for "@type": "BreadcrumbList"
  e.g., 2022/04/how-to-create-your-own-nft-generative-art-collections-with-python/
- In post and tag page e.g., tag/automate/ look for script type="application/ld+json" and "@type": "CollectionPage"

# HOW_TO_2: Validate with Google's Rich Results Test
- Go to: https://search.google.com/test/rich-results
- Enter your post URL (or paste the HTML source)
- Click "Test URL"

# HOW_TO_3: Test with Schema.org Validator
- Go to: https://validator.schema.org/
- Paste your post's HTML source
- Check for errors
```

---

## Automation Philosophy

Try to automate as much as possible, especially time-consuming tasks that you will have to do repeatedly.

### Example: Database Import Script
```bash
#!/bin/bash

# IMPORT .SQL INTO DOCKERIZED MYSQL FOR WORDPRESS
# Usage: ./import_wordpress_db.sh

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker and try again."
    exit 1
fi

# 1. Create database wordpress2
echo "Creating database 'wordpress2'..."
docker exec wp_docker-db-1 mysql -u root -proot -e "CREATE DATABASE IF NOT EXISTS wordpress2 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" || {
    echo "Error: Failed to create database."
    exit 1
}

# 2. Import SQL file
SQL_FILE="/Users/brunoflaven/Documents/01_work/blog_articles/_ia_augmented_journalist_wp_toolkit/4fe6ae31-f930-4ae6-87eb-04edd2efbb6e-mysql716.flavenmod1.2026-01-12-14h43.sql"
if [ ! -f "$SQL_FILE" ]; then
    echo "Error: SQL file not found at $SQL_FILE"
    exit 1
fi
echo "Importing database... this may take 5-15 minutes..."
docker exec -i wp_docker-db-1 mysql -u root -proot wordpress2 < "$SQL_FILE" || {
    echo "Error: Failed to import SQL file."
    exit 1
}

# 3. Update site URLs
echo "Updating site URLs..."
docker exec wp_docker-db-1 mysql -u root -proot wordpress2 -e "UPDATE wp_options SET option_value = 'http://localhost:8080' WHERE option_name IN ('siteurl', 'home');" || {
    echo "Error: Failed to update site URLs."
    exit 1
}

# 4. Verify import
echo "Verifying import..."
docker exec wp_docker-db-1 mysql -u root -proot wordpress2 -e "SELECT COUNT(*) as tables FROM information_schema.tables WHERE table_schema = 'wordpress2';"
docker exec wp_docker-db-1 mysql -u root -proot wordpress2 -e "SELECT COUNT(*) as posts FROM wp_posts WHERE post_type = 'post' AND post_status = 'publish';"
docker exec wp_docker-db-1 mysql -u root -proot wordpress2 -e "SELECT COUNT(*) as tags FROM wp_term_taxonomy WHERE taxonomy = 'post_tag';"

echo "Import complete!"
```

---

## Motivation: Create a Motto

> **Discuss, Design, Develop, Decide, DELIVER... and then celebrate.**

---

## Documentation: Write for a Seven-Year-Old (As Persona)

### Tone & Style: Write Like a Story
- Narrative Flow: Treat it like a journal or case study—not a dry manual
- Simple Language: Avoid jargon
- Personal Touch: Add anecdotes

### Structure: Chronological + Practical
- Timeline (The "Story" Part)
- Key Sections (The "How-To" Part)

---

## Plugin Blueprint: AI-Augmented Tagging

I am dealing with **RELATED_TAGS** or **Tag Families**. Here is a blueprint for the WordPress plugin that helps users pick the right tags for their blog posts, using AI and "named entities" (like people, places, or products mentioned in the text).

### CSV Structure for Tag Families

| Column | Description | Example |
|--------|-------------|---------|
| family_id | Family (cluster) ID | 0 |
| canonical_tag_id | WordPress tag ID representing the family (the "parent") | 6 |
| canonical_label | Name of the parent tag | information |
| tag_id | ID of a family member (can be the parent or a child) | 8 |
| tag_label | Name of the member tag | infosuroit |
| similarity_to_canonical | Semantic similarity to the parent (0 to 1) | 0.804 |
| usage_count | Number of posts using this tag | 5 |
| entity_label | NER entity type (see table below) | O |

### Entity Types (entity_label)
- **O** – Outside (no special type) e.g., information, marketing, data
- **PERSON** – Person e.g., jackson, robert jackson, susan jackson
- **ORG** – Organization e.g., Adobe, 3WDOC, POC
- **GPE** – Geopolitical entity e.g., Paris, France, New York
- **CARDINAL** – Number e.g., 2012, 3, 100
- **DATE** – Date e.g., January 2024, 2012
- **PRODUCT** – Product e.g., Adsense, Photoshop

### Key Rules
1. Each family has **ONLY ONE** canonical_tag_id (the parent)
2. The canonical_label is **IDENTICAL** for all family members
3. The canonical tag appears as the first row (similarity = 1.0)
4. similarity_to_canonical: 1.0 = identical, <1.0 = similar

---

## Using Docker for Staging WordPress

```bash
cd /Users/brunoflaven/Documents/01_work/blog_articles/_ia_3d_architecture_ocr/ia_wp_plugin_related_content_steps
mkdir wp_docker
cd wp_docker

docker compose down
docker compose up -d

# All should be "Up"
docker compose ps

# Should show MySQL ready
docker compose logs db

# WordPress: http://localhost:8080
# phpMyAdmin: http://localhost:8081
```

---

## WordPress REST API Queries

To build effective AI applications, you need content—and ideally, structured content. The WordPress REST API provides exactly that.

```
# Some queries on WP API
# Base: https://your-site.com/wp-json/wp/v2/

# Get all posts
GET /wp-json/wp/v2/posts

# Get single post
GET /wp-json/wp/v2/posts/{id}

# Create post (requires authentication)
POST /wp-json/wp/v2/posts

# Pagination
?per_page=10&page=2

# Search
?search=keyword

# Filter by category
?categories=5

# Order
?orderby=date&order=desc
```

---

## Using Mistral OCR

```bash
# Install the environment
conda create -n mistral -y python=3.9
conda activate mistral
pip install mistralai python-dotenv datauri

# You need a PRODUCTION KEY for Mistral OCR
# Example: XXX-fake-mistral-ocr-api-key-7Df
```

- [Mistral OCR Documentation](https://docs.mistral.ai/capabilities/document_ai/basic_ocr)

---

# Challenges in Training Whisper for Custom Languages

## The Linguistic Landscape: Key African Languages

| Language | Speakers (approx.) | Regions & Diaspora |
|----------|---------------------|--------------------|
| Yoruba   | 30 million          | Nigeria, Benin, Togo |
| Oromo    | 30 million          | Ethiopia |
| Igbo     | 24 million          | Nigeria |
| Zulu     | 12 million          | South Africa |
| Lingala  | 10 million          | DRC, Republic of Congo |
| Wolof    | 9.4 million         | Senegal (85% of population) |
| Somali   | 28 million          | Somalia, Somaliland, Djibouti, Ethiopia, Kenya |
| Kirundi  | 12 million          | Burundi, Rwanda, Tanzania, DRC, Uganda |
| Amharic  | 10 million          | Ethiopia |
| Tigrinya | 1.6 million         | Eritrea (50% of population) |

These languages, while rich and diverse, pose significant challenges for speech recognition models due to limited training data and dialectal variations.

---

## Case Studies: The Challenges of Multilingual Speech Recognition

### 1. Tunisian Dialect (DJO Project)
- **Problem:** Tunisian Arabic is a dialectal variant of Arabic, distinct from Modern Standard Arabic (MSA). Existing models like Whisper struggle to accurately transcribe Tunisian due to its unique vocabulary, pronunciation, and lack of standardized written form.
- **Solution:** The AI platform [DJO](https://akademie.dw.com/en/an-ai-platform-wins-top-2025-media-loves-tech-prize/a-75134414), winner of the 2025 Media Loves Tech Grand Prize, was developed to address this gap.

### 2. Senegalese Languages (Wolof, Diola, Fulfude)
- **Problem:** In Senegal, multilingualism is common, with Wolof, Diola, and Fulfude (Peul) spoken alongside French and English. Whisper and other models often fail to distinguish between these languages or accurately transcribe them, especially in code-switching scenarios.
- **Impact:** Poor transcription quality limits the usability of voice-based applications, such as chatbots or media subtitling, for local populations.

### 3. Multilingual Challenges (Mandenkan, Fulfude, Hausa, Kiswahili)
- **Problem:** International media (e.g., radio, television) broadcast in multiple African languages, including Mandenkan, Fulfude, Hausa, and Kiswahili. Whisper's performance is inconsistent across these languages, particularly for named entities (e.g., proper nouns, locations).
- **Root Cause:** The lack of high-quality, language-specific training data and the complexity of dialectal variations.

---

## Technical Insights: Testing Whisper and Alternatives

### Test Results Summary
- **Whisper Large, Custom Implementation:** Achieved the best transcription results among the tested models.
- **MMS by Facebook AI:** Despite supporting over 1,000 languages (including Swahili), the transcription quality was disappointing.
- **Fine-tuned Whisper Large & Small:** Both performed poorly, likely due to insufficient training data or suboptimal fine-tuning processes.

### Key Observations
- **Training Complexity:** Fine-tuning Whisper for low-resource languages is technically demanding. Success depends on the quality and quantity of the training corpus.
- **Named Entity Recognition:** Even with a robust transcription model, poor transcription quality undermines named entity recognition.
- **Post-Processing Limitations:** While post-processing can improve results, it cannot fully compensate for fundamental transcription errors.

---

## Conclusion: The Path Forward

### Immediate Solution
- **Status Quo:** Continue using Whisper Large with the current implementation, supplemented by post-processing where possible.

### Long-Term Goal
- **Custom Training:** Train Whisper Large on domain-specific datasets (e.g., Swahili content) to significantly improve transcription accuracy.
- **Named Entity Improvement:** Refine the list of named entities (tags) for better editorial accuracy, though transcription quality remains the primary bottleneck.

### Final Thought
Without access to better models or the ability to train on dedicated, high-quality datasets, the current implementation of Whisper Large remains the most viable option. However, the ultimate goal is to bridge the gap for African and dialectal languages through targeted training and community-driven data collection.
