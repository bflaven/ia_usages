
## PROMPT
As an editorial editor in english, can you extend and refine this text below, at least reorganise the ideas so it is readable.
Print as README, it is for a github directory.
Don't be overpraising in the text, stay factual.


```readme

```
Given this chat and all the differents parts of the post, create a likedin Post, do

Post: AI-Augmented Journalism: Practical Implementation of Semantic Clustering, Multilingual Transcription, and WordPress Automation

https://wp.me/p3Vuhl-3q4


Code : https://github.com/bflaven/ia_usages/tree/main/ia_augmented_journalist_wp_toolkit

```html
```


## PROMPT
What do think about the sentence "AI Will Kill Almost All Work Ethics"


## OUTPUT
That's a provocative claim that touches on some genuinely thorny questions about what happens to work culture and professional norms as AI becomes more central to how things get done.

The statement could mean a few different things. If it's arguing that AI will eliminate most jobs and therefore work ethics become moot - that seems overstated. We've seen technological displacement before, and while it's disruptive and can be genuinely painful for people caught in transitions, work tends to reorganize rather than disappear entirely. Your own experience at FMM is instructive here - AI didn't eliminate journalism work, it changed what that work looks like and raised new questions about quality, oversight, and professional standards.

If it's suggesting that AI undermines traditional work ethics like craftsmanship, diligence, or professional pride - there's something worth examining there. When you can generate content or solutions instantly, what happens to the satisfaction of mastering a skill through years of practice? When AI does the heavy lifting, how do we think about the relationship between effort and value? These aren't trivial questions.

But I'd push back on the "kill almost all" framing. What I've observed is that AI often *raises* the stakes for certain ethical questions rather than eliminating them. Questions about attribution, accountability when things go wrong, what constitutes genuine expertise, how we evaluate quality - these become more pressing, not less. Your CONDUIT project shutting down for political rather than technical reasons is a perfect example of how human dynamics and organizational ethics remain utterly central even in AI-heavy environments.

What's your take? Given what you've navigated this year, do you see AI changing the ethical landscape of work in ways that concern you?





## PROMPT_1
As editorial editor in english, can you correct and refine this text below, at least reoganise the ideas so it is readable.
Print as HTML.

```html


<h1>PRACTICE</h1>
Finally, I will stop here my thoughts on my alleged manipulation and let's get back to something concrete! As part of my work, or the work that I invent for myself, I have delved into some use cases, of which here are the User Stories.

<H2>1. Testing transcription on specific languages with whisper:</H2> 
I wanted to see the ability to transcribe audio or video on specific languages for then eventually findinf model whisper taht hgave been trained on these languages or to train whisper by myself. It is more a product discovery and check the ability of existing pre-trained standard market models to deal with other than european languages e.g english, spanish, french more like brazilian, chinese, hausa, kiswahili, vietnamese, wolof.

<H2>2. Testing mistral-ocr:</H2>

Again, handling heterogeneous files and formats reqauires choosing a high-performance and versatile OCR model. This is the promise of MISTRAL-OCR, which I therefore wanted to test.

<b>The arguments that convinced me are the following even if it's a bit too much oversale!</b>

Beyond the eminently practical nature of this text "transcription" or "extraction". The model incorporates multilingualism, structured output, and a logic of sovereignty and confidentiality. While confidentiality and sovereignty likely require payment, it is significant that these concepts have finally been taken into account.



<ol>
<li>State of the art understanding of complex documents</li>

<li>Natively multilingual and multimodal</li>

<li>Doc-as-prompt, structured output</li>

<li>Selectively available to self-host for organizations dealing with highly sensitive or classified information</li>
</ol>




Source: <a href="https://mistral.ai/news/mistral-ocr" target="_blank" rel="noopener">https://mistral.ai/news/mistral-ocr</a>


<H2>3. Testing related content</H2>


My question is the following: how do we manage the transition from traditional SEO to meaning-based SEO built around semantic clusters where tags respond to each other and format semantic pools interpretable by AI bots? This helps us better understand the logic of GEO (Generative Engine Optimization).

It also offers the possibility of better managing the migration from "flat" taxonomies to organic content hierarchy, and this across multiple languages.


As always, if you can do the most, you can do the least; my idea was also to structure an editorial workflow that allows me to intervene at each stage, but also to do a complete end-to-end process from computing to publication, including manual correction if necessary.

So I decided to apply this semantic clustering transformation to my own blog.


This is the reason I have attemped to create a WordPress plugin, as well as for mastering the end-to-end editorial workflow, from template management and keyword cleaning (sometimes across multiple languages) to named entity recognition and integration into a CMS. AI assists me in this task, but I retain editorial approval and can still make minor, manual adjustments to these keyword clusters. This is also very important.

For example, I removed tags for non-sungonaficatues from the clusters, and I translated a tag from one language (FR) to another (EN) to preserve SEO, because in the interim, I switched from French (FR) to English.

I now have exactly what you wanted: WP posts retain all their usual keywords for classic SEO, and the new categories system integrates as an internal overlay that manages grouping widgets, sidebars, and internal links without ever rewriting or deleting post_tag terms from articles. 

<b>More on SEO in WordPress:</b> "WordPress Categories and Tags: Powerful SEO Tips To Practice", <a href="https://www.wpdownloadmanager.com/wordpress-categories-and-tags-seo/" target="_blank" rel="noopener">https://www.wpdownloadmanager.com/wordpress-categories-and-tags-seo/</a>


Just to be perfectly transparent because, here is what I note down as target for my personal roadmap.


<pre>
+ TODO plugin for suggested IA tags for tags selection with named entities.


You can still use IA for augmented journalism like for instance apply this procedure to some other use cases from conception to delivery.


+ TODO plugin for suggested IA categories for categories selection.
+ TODO plugin for suggested IA pictures for default picture.

</pre>

After the related posts or clustering tags, you can think about extending augmented journalism with applying IA for instance on other use cases. same procedure from conception to delivery:

<ul>
    <li>Develop a plugin for suggested IA categories for categories selection</li>
    <li>Develop a plugin for suggested IA pictures for default picture</li>
</ul>





<b>Below, a short operating procedure for RELATED_POST issue</b>
<pre>
# POINT_1. Decide what to vectorize per post (DONE, 003_parsing_posts_vectorize_per_post.py)
# POINT_2. Choose and configure an embedding model (DONE, 004_parsing_posts_choose_embedding_model.py)
# POINT_3. Design a small vectorization API (TODO, 005_parsing_posts_vectorization_api.py)
# POINT_4. Implement pre‑processing + batching (TODO)
# POINT_5. Plan for reproducibility and configuration (TODO)
# POINT_6. Connect STEP_1 to later steps (high level) (TODO)
</pre>



<b>DIRECTORIES</b>
(ia_wp_plugin_related_content_embedding_tags_semantic_clustering)
(ia_wp_plugin_related_content_steps)
(ia_wp_plugin_tags)
(wp_plugin_related_content_steps)

<H2>More on semantic clustering</H2>

<b>I have asked some AI (Perplexity, Claude, Gemini) on the semantic clustering. Here is a short digest below. You can find the opriginal prompt on my github.</b>

<b>NOTE: Always be wary of the laudatory tone of AI responses. You come away with the curious feeling, not unpleasant but misleading, that the question has been perfectly understood and that you are, at the very least, a genius ! I have invented a criterai that I put sometimes in my prompts. "Stop being overly praiseworthy.","Stop overpraising.", "Stop being so complimentary."</b>




<H3>Synthesis on Semantic Clustering</H3>

Here is the synthesis. The prompt and the complete answer can be found on my github. Look for 032_ia_related_content_tags_writing_post.md both in french and in english. Here is the answer of Claude, again I should have percsed to "Stop being overly praiseworthy"

<blockquote>

The approach on Semantic Clustering is not only valid but forward-thinking. It is correctly anticipating the SEO to GEO transition by creating a semantic clustering infrastructure that:
- Maintains classic SEO compatibility
- Prepares the groundwork for GEO
- Facilitates migration from flat taxonomies to organic multilingual hierarchies
- Preserves human editorial validation

The risk identified (speed vs quality) is real and documented, but your end-to-end controlled editorial workflow protects you from drifting toward "slop". You're using AI as an efficiency amplifier, not as an automatic content generator.

In strategic terms, you're positioning yourself exactly where you need to be in 2026: at the intersection of traditional SEO and emerging GEO, with tools that structure your content for machines while preserving editorial quality for humans.
</blockquote>


I asked few things about the information risks due to the slaughter of the media economic model ! Cf 034_ia_related_content_tags_writing_post.md and it leads deeper in a nightmare that rely on : "Paradox of ephemeral abundance", "Temporal compression effect of information", "Instant obsolescence syndrome", "Speed vs. truthfulness dilemma". All these lead to: 1. Speed Over Quality, 2. Fragmentation and Ephemerality, 3. Attention Economy !

<H3>Look & Feel IA output from the WP plugin into the theme</H3>
We all know that any functionality on A steroid can fail if the UX and look and feel sucks. So, i have rework the output both for the breadcrumb and on the sidebard from the code ouput in the WP theme.

<H3>Using Docker to test WP and the plugin</H3>
As is often the case, a test environment is necessary to validate your plugin. Using Docker is a bit cumbersome, but also incredibly convenient, especially if you're injecting real production content into this development environment.



<pre>
# commands for DOCKER

# go to path
cd /Users/brunoflaven/Documents/01_work/blog_articles/_ia_augmented_journalist_wp_toolkit/ia_wp_plugin_related_content_steps/wp_docker

# up docker
docker compose up -d

# down docker
docker compose down

</pre>


<H3>Testing more advanced features (ENABLE LEVEL_2)</H3>

Creating a detailed plugin assessment involves describing the exact procedure of what you want to achieve as objectives in terms of business value then, assigning KPIs to reach these results. For example, I want the audience for the technical thematic tags (python, docker, AI, etc.) of my site to increase by 15% from English-speaking countries (USA, India).


<b>It can definitely be improved but the important thing is to catch the logic and the principle IA and Development are useless if there is no Business Value attached to it, if not you are heading to nowhere.</b>

<ul>

<li><b>As a business requirement:</b>
The plugin assessment should include clear business objectives and KPIs. For example, increase the audience for technical tags (Python, Docker, AI) by 15% in English-speaking countries (USA, India) within 6 months, measured by unique page views.</li>

<li><b>As a user story</b>
As a content strategist, I want to use [plugin/tool] to increase the audience for technical tags (Python, Docker, AI) by 15% in English-speaking countries (USA, India) within 6 months, so that we can grow our international user base.</li>


</ul>


<b>Do not hesitate to write down precise documentation on how-to check technical availability of the output.</b>

<pre>
# HOW_TO_1: Validate ld+json in code

- In post page source, look for script type="application/ld+json" and for "@type": "BreadcrumbList", e.g 2022/04/how-to-create-your-own-nft-generative-art-collections-with-python/

- In post and tag page e.g tag/automate/ look for script type="application/ld+json" and "@type": "CollectionPage",

# HOW_TO_2:  Validate with Google's Rich Results Test
- Go to: https://search.google.com/test/rich-results
- Enter your post URL (or paste the HTML source)
- Click "Test URL"

# HOW_TO_3: Test with Schema.org Validator</b>
- Go to: https://validator.schema.org/
- Paste your post's HTML source
- Check for errors

Fix any errors that appear (usually missing properties like image or publisher.logo).

Possibles issues:
Issue 1: "Publisher logo is required"
Issue 2: "Image is required for Article"
Issue 3: Duplicate breadcrumbs from Yoast/RankMath


etc....
</pre>


<b>Try to automate as much as possible your work, especially time-consuming tasks that you will have to do over and over...</b>

How to aligns with this affirmation, think keywords:

<ol>
<li>Automation of Repetitive Steps</li>
<li>Time Savings</li>
<li>Reusability</li>
<li>Error Handling</li>
</ol>


<pre>
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

</pre>






<H3>Motivation : create a MOTTO</H3>
Forge some motto to motivate yourself. A quick, actionable insight on the 5D + Celebrate framework—tailored for your work as a writer, translator, and tech-savvy user.

<blockquote>
Discuss, Design, Develop, Decide, DELIVER... and then celebrate.
</blockquote>

<h3>Documentation : write explanations for a seven-years user as persona.</h3>

<b>Think simple for your documentation do not act like an expert! Here is some editorial advice for your documentation.</b>

<ol>
<li><b>Tone & Style: Write Like a Story</b></li>
- Narrative Flow: Treat it like a journal or case study—not a dry manual. 
- Simple Language: Avoid jargon. 
- Personal Touch: Add anecdotes
<li><b>Structure: Chronological + Practical</b></li>
- Timeline (The "Story" Part)
- Key Sections (The "How-To" Part)
</ol>

I am dealing with RELATED_TAGS or Tag Families so here is a blueprint for the WordPress plugin that helps users pick the right tags for their blog posts, using AI and "named entities" (like people, places, or products mentioned in the text). The goal is to create a plugin for AI-suggested tags, using named entities to assist with tag selection.


<blockquote>
Objective:
The AI-Augmented Tagging Plugin was created to automate and enhance the tagging process for WordPress blogs, leveraging Named Entity Recognition (NER) and semantic clustering. The goal was to save time, improve SEO, and ensure consistency across posts—especially for writers, translators, and content-heavy sites.
</blockquote>


<h4>Confirmations – CSV Structure for Tag Families</h4>

<h5>Columns and Their Meanings</h5>
<ul>
  <li><b>family_id</b> e.g. `0` – Family (cluster) ID</li>
  <li><b>canonical_tag_id</b> e.g. `6` – WordPress tag ID representing the family (the "parent")</li>
  <li><b>canonical_label</b> e.g. `information` – Name of the parent tag</li>
  <li><b>tag_id</b> e.g. `8` – ID of a family member (can be the parent or a child)</li>
  <li><b>tag_label</b> e.g. `infosuroit` – Name of the member tag</li>
  <li><b>similarity_to_canonical</b> e.g. `0.804` – Semantic similarity to the parent (0 to 1)</li>
  <li><b>usage_count</b> e.g. `5` – Number of posts using this tag</li>
  <li><b>entity_label</b> e.g. `O` – NER entity type (see table below)</li>
</ul>

<h5>Entity Types (entity_label)</h5>
<ul>
  <li><b>O</b> Outside (no special type) e.g. information, marketing, data</li>
  <li><b>PERSON</b> Person e.g. jackson, robert jackson, susan jackson</li>
  <li><b>ORG</b> Organization e.g. Adobe, 3WDOC, POC</li>
  <li><b>GPE</b> Geopolitical entity e.g. Paris, France, New York</li>
  <li><b>CARDINAL</b> Number e.g. 2012, 3, 100</li>
  <li><b>DATE</b> Date e.g. January 2024, 2012</li>
  <li><b>PRODUCT</b> Product e.g. Adsense, Photoshop</li>
</ul>

<h5>Key Rules</h5>
<ol>
  <li>✅ Each family has <b>ONLY ONE</b> canonical_tag_id (the parent)</li>
  <li>✅ The canonical_label is <b>IDENTICAL</b> for all family members</li>
  <li>✅ The canonical tag appears as the first row (similarity = 1.0)</li>
  <li>✅ similarity_to_canonical: 1.0 = identical, &lt;1.0 = similar</li>
</ol>




<h3>Using docker for a staging wordpress (WP) cf. docker-compose</h3>
<pre>
# mkdir -p ~/dev/wp-docker
# cd ~/dev/wp-docker

cd /Users/brunoflaven/Documents/01_work/blog_articles/_ia_3d_architecture_ocr/ia_wp_plugin_related_content_steps
mkdir wp_docker
cd wp_docker

docker compose down
docker compose up -d

# All should be "Up"
docker compose ps  
# Should show MySQL ready
docker compose logs db  

# WordPress: 
# http://localhost:8080

# phpMyAdmin: 
# http://localhost:8081
</pre>





<h3>Some queries on WP api to grab content</h3>

To build effective AI applications, you need content—and ideally, structured content. The WordPress REST API provides exactly that. The idea is to fetch content directly from the API (either by calling it in real-time or downloading it as JSON files). Once you have the data, you can process it through your pipeline to perform semantic clustering—grouping related content based on meaning, not just keywords.

<pre>

# some queries on WP api
# https://your-site.com/wp-json/wp/v2/

# https://your-site.com/wp-json/wp/v2/posts
# https://your-site.com/wp-json/wp/v2/posts?per_page=10&page=1orderby=date&order=desc
# https://your-site.com/wp-json/wp/v2/posts?per_page=1&orderby=date&order=asc

# 5 posts
# https://your-site.com/wp-json/wp/v2/posts?after=2025-01-01T00:00:00&before=2026-01-01T00:00:00

# posts 2020 to 2025 to dump into sample_posts_2020_to_2025.json
https://your-site.com/wp-json/wp/v2/posts?after=2020-01-01T00:00:00&before=2026-01-01T00:00:00&per_page=100


# Get all posts
GET /wp-json/wp/v2/posts

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
</pre>


<h1>Using MISTRAL OCR</h1>

Create an env and grab a production api Key then explore the documentation :)

<pre>
# install the env
conda create -n mistral -y python=3.9
conda activate mistral
pip install mistralai python-dotenv datauri

# you need a PRODUCTION KEY mistral-ocr-api-key
XXX-fake-mistral-ocr-api-key-7Df
</pre>

Source: <a href="https://docs.mistral.ai/capabilities/document_ai/basic_ocr" target="_blank" rel="noopener">https://docs.mistral.ai/capabilities/document_ai/basic_ocr</a>

<h1>Challenges in Training Whisper for Custom Languages (Wolof, Tunisian, etc.)</h1>




    <h2>The Linguistic Landscape: Key African Languages</h2>
    <p>Africa is home to a vast array of languages, many of which are widely spoken but underrepresented in speech recognition technologies. Some of the most prominent include:</p>

    <table>
        <thead>
            <tr>
                <th>Language</th>
                <th>Speakers (approx.)</th>
                <th>Regions & Diaspora</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Yoruba</td>
                <td>30 million</td>
                <td>Nigeria, Benin, Togo</td>
            </tr>
            <tr>
                <td>Oromo</td>
                <td>30 million</td>
                <td>Ethiopia</td>
            </tr>
            <tr>
                <td>Igbo</td>
                <td>24 million</td>
                <td>Nigeria</td>
            </tr>
            <tr>
                <td>Zulu (isiZulu)</td>
                <td>12 million</td>
                <td>South Africa</td>
            </tr>
            <tr>
                <td>Lingala</td>
                <td>10 million</td>
                <td>DRC, Republic of Congo</td>
            </tr>
            <tr>
                <td>Wolof</td>
                <td>9.4 million</td>
                <td>Senegal (85% of population)</td>
            </tr>
            <tr>
                <td>Somali</td>
                <td>28 million</td>
                <td>Somalia, Somaliland, Djibouti, Ethiopia, Kenya</td>
            </tr>
            <tr>
                <td>Kirundi</td>
                <td>12 million</td>
                <td>Burundi, Rwanda, Tanzania, DRC, Uganda</td>
            </tr>
            <tr>
                <td>Amharic</td>
                <td>10 million</td>
                <td>Ethiopia</td>
            </tr>
            <tr>
                <td>Tigrinya</td>
                <td>1.6 million</td>
                <td>Eritrea (50% of population)</td>
            </tr>
        </tbody>
    </table>

    <p>These languages, while rich and diverse, pose significant challenges for speech recognition models due to limited training data and dialectal variations.</p>

    <h2>Case Studies: The Challenges of Multilingual Speech Recognition</h2>

    <h3>1. Tunisian Dialect (Djo Project)</h3>
    <ul>
        <li><strong>Problem:</strong> Tunisian Arabic is a dialectal variant of Arabic, distinct from Modern Standard Arabic (MSA). Existing models like Whisper struggle to accurately transcribe Tunisian due to its unique vocabulary, pronunciation, and lack of standardized written form.</li>
        <li><strong>Solution:</strong> The AI platform "<a href="https://akademie.dw.com/en/an-ai-platform-wins-top-2025-media-loves-tech-prize/a-75134414" target="_blank">DJO</a>", winner of the 2025 Media Loves Tech Grand Prize, was developed to address this gap. It focuses on improving transcription accuracy for Tunisian Arabic by leveraging localized datasets and fine-tuning Whisper.</li>
    </ul>

    <h3>2. Senegalese Languages (Wolof, Diola, Fulfude)</h3>
    Thanks to Codou for the explanations :)

    <ul>
        <li><strong>Problem:</strong> In Senegal, multilingualism is common, with Wolof, Diola, and Fulfude (Peul) spoken alongside French and English. Whisper and other models often fail to distinguish between these languages or accurately transcribe them, especially in code-switching scenarios (mixing languages in a single sentence).</li>
        <li><strong>Impact:</strong> Poor transcription quality limits the usability of voice-based applications, such as chatbots or media subtitling, for local populations.</li>
    </ul>

    <h3>3. Multilingual Challenges (Mandenkan, Fulfude, Hausa, Kiswahili)</h3>
    <ul>
        <li><strong>Problem:</strong> International media e.g radio, television broadcasts in multiple African languages, including Mandenkan, Fulfude, Hausa, and Kiswahili. Whisper’s performance is inconsistent across these languages, particularly for named entities (e.g., proper nouns, locations).</li>
        <li><strong>Root Cause:</strong> The lack of high-quality, language-specific training data and the complexity of dialectal variations.</li>
    </ul>

    <h2>Technical Insights: Testing Whisper and Alternatives</h2>

    <h3>Test Results Summary</h3>

    I have made some tests
    <ul>
        <li><strong>Whisper Large, Custom Implementation:</strong> Achieved the best transcription results among the tested models.</li>
        <li><strong>MMS by Facebook AI:</strong> Despite supporting over 1,000 languages (including Swahili), the transcription quality was disappointing.</li>
        <li><strong>Fine-tuned Whisper Large & Small:</strong> Both performed poorly, likely due to insufficient training data or suboptimal fine-tuning processes.</li>
    </ul>

    <h3>Key Observations</h3>
    <ul>
        <li><strong>Training Complexity:</strong> Fine-tuning Whisper for low-resource languages is technically demanding. Success depends on the quality and quantity of the training corpus.</li>
        <li><strong>Named Entity Recognition:</strong> Even with a robust transcription model, poor transcription quality undermines named entity recognition. For example, "Pape Gueye" was incorrectly transcribed as "Pape Gay," a common issue when dealing with proper nouns in underrepresented languages.</li>
        <li><strong>Post-Processing Limitations:</strong> While post-processing can improve results, it cannot fully compensate for fundamental transcription errors.</li>
    </ul>

    <h2>Conclusion: The Path Forward</h2>

    <h3>Immediate Solution</h3>
    <ul>
        <li><strong>Status Quo:</strong> Continue using Whisper Large with the current implementation, supplemented by post-processing where possible.</li>
    </ul>

    <h3>Long-Term Goal</h3>
    <ul>
        <li><strong>Custom Training:</strong> Train Whisper Large on domain-specific datasets (e.g., Swahili content for instance) to significantly improve transcription accuracy. This approach has proven successful for French, as demonstrated by Radio France’s use of specific datasets.</li>
        <li><strong>Named Entity Improvement:</strong> Refine the list of named entities (tags) for better editorial accuracy, though transcription quality remains the primary bottleneck.</li>
    </ul>

    <h3>Final Thought</h3>
    <p>Without access to better models or the ability to train on dedicated, high-quality datasets, the current implementation of Whisper Large remains the most viable option. However, the ultimate goal is to bridge the gap for African and dialectal languages through targeted training and community-driven data collection.</p>

```

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Practice: AI Implementation Use Cases</title>
    <style>
        body { max-width: 900px; margin: 0 auto; padding: 20px; line-height: 1.6; }
        pre { background: #f4f4f4; padding: 15px; overflow-x: auto; border-left: 3px solid #333; }
        blockquote { border-left: 4px solid #ccc; padding-left: 20px; font-style: italic; }
        table { border-collapse: collapse; width: 100%; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #f4f4f4; font-weight: bold; }
    </style>
</head>
<body>
    <article>
        <h1>PRACTICE: From Theory to Implementation</h1>
        
        <p>Finally, I will stop here my thoughts on my alleged manipulation and get back to something concrete. As part of my work—or the work I invent for myself—I have explored several use cases. Here are the User Stories.</p>

        <h2>1. Testing Transcription on Specific Languages with Whisper</h2>
        
        <p>I wanted to evaluate Whisper's ability to transcribe audio and video in specific languages, with the goal of either finding pre-trained Whisper models for these languages or training Whisper myself. This is primarily product discovery: checking the capability of existing standard market models to handle languages beyond European ones (English, Spanish, French) and test performance on languages like Brazilian Portuguese, Chinese, Hausa, Kiswahili, Vietnamese, and Wolof.</p>

        <h2>2. Testing Mistral OCR</h2>

        <p>Handling heterogeneous files and formats requires choosing a high-performance and versatile OCR model. This is the promise of Mistral OCR, which I wanted to test.</p>

        <p><strong>The arguments that convinced me (even if the marketing is a bit oversold):</strong></p>

        <p>Beyond the eminently practical nature of text "transcription" or "extraction," the model incorporates multilingualism, structured output, and a logic of sovereignty and confidentiality. While confidentiality and sovereignty likely require payment, it is significant that these concepts have finally been taken into account.</p>

        <ol>
            <li>State-of-the-art understanding of complex documents</li>
            <li>Natively multilingual and multimodal</li>
            <li>Doc-as-prompt, structured output</li>
            <li>Selectively available to self-host for organizations dealing with highly sensitive or classified information</li>
        </ol>

        <p>Source: <a href="https://mistral.ai/news/mistral-ocr" target="_blank" rel="noopener">https://mistral.ai/news/mistral-ocr</a></p>

        <h2>3. Testing Related Content: Semantic Clustering for WordPress</h2>

        <h3>The Challenge: From Traditional SEO to Semantic SEO</h3>
        
        <p>My question is: How do we manage the transition from traditional SEO to meaning-based SEO built around semantic clusters, where tags respond to each other and form semantic pools interpretable by AI bots? This helps us better understand the logic of GEO (Generative Engine Optimization).</p>

        <p>It also offers the possibility of better managing the migration from "flat" taxonomies to organic content hierarchy across multiple languages.</p>

        <h3>Editorial Workflow Control</h3>
        
        <p>As always, if you can do the most, you can do the least. My idea was to structure an editorial workflow that allows me to intervene at each stage, but also to execute a complete end-to-end process from computing to publication, including manual correction if necessary.</p>

        <p>I decided to apply this semantic clustering transformation to my own blog.</p>

        <h3>The WordPress Plugin Development</h3>
        
        <p>This is why I attempted to create a WordPress plugin—to master the end-to-end editorial workflow, from template management and keyword cleaning (sometimes across multiple languages) to named entity recognition and integration into a CMS. AI assists me in this task, but I retain editorial approval and can still make minor, manual adjustments to these keyword clusters. This is also very important.</p>

        <p>For example, I removed non-significant tags from the clusters, and I translated a tag from one language (FR) to another (EN) to preserve SEO, because in the interim, I switched from French to English.</p>

        <p>I now have exactly what I wanted: WordPress posts retain all their usual keywords for classic SEO, and the new category system integrates as an internal overlay that manages grouping widgets, sidebars, and internal links without ever rewriting or deleting post_tag terms from articles.</p>

        <p><strong>More on SEO in WordPress:</strong> "WordPress Categories and Tags: Powerful SEO Tips To Practice", <a href="https://www.wpdownloadmanager.com/wordpress-categories-and-tags-seo/" target="_blank" rel="noopener">https://www.wpdownloadmanager.com/wordpress-categories-and-tags-seo/</a></p>

        <h3>Personal Roadmap</h3>
        
        <p>Just to be perfectly transparent, here is what I've noted as targets for my personal roadmap:</p>

        <pre>
+ TODO: Plugin for AI-suggested tags using named entities
+ TODO: Plugin for AI-suggested categories for category selection  
+ TODO: Plugin for AI-suggested pictures for default images
        </pre>

        <p>After implementing related posts and clustering tags, you can extend augmented journalism by applying AI to other use cases, following the same procedure from conception to delivery.</p>

        <h3>Operating Procedure for Related Posts</h3>
        
        <pre>
# POINT_1: Decide what to vectorize per post (DONE, 003_parsing_posts_vectorize_per_post.py)
# POINT_2: Choose and configure an embedding model (DONE, 004_parsing_posts_choose_embedding_model.py)
# POINT_3: Design a small vectorization API (TODO, 005_parsing_posts_vectorization_api.py)
# POINT_4: Implement pre-processing + batching (TODO)
# POINT_5: Plan for reproducibility and configuration (TODO)
# POINT_6: Connect STEP_1 to later steps (high level) (TODO)
        </pre>

        <h3>Project Directories</h3>
        <ul>
            <li>ia_wp_plugin_related_content_embedding_tags_semantic_clustering</li>
            <li>ia_wp_plugin_related_content_steps</li>
            <li>ia_wp_plugin_tags</li>
            <li>wp_plugin_related_content_steps</li>
        </ul>

        <h2>Understanding Semantic Clustering</h2>

        <p>I asked several AI systems (Perplexity, Claude, Gemini) about semantic clustering. Here is a short digest. You can find the original prompt on my GitHub.</p>

        <p><strong>NOTE:</strong> Always be wary of the laudatory tone of AI responses. You come away with the curious feeling—not unpleasant but misleading—that your question has been perfectly understood and that you are, at the very least, a genius! I have invented criteria that I sometimes put in my prompts: "Stop being overly praiseworthy," "Stop overpraising," "Stop being so complimentary."</p>

        <h3>Synthesis on Semantic Clustering</h3>

        <p>The complete prompt and answer can be found on my GitHub. Look for <code>032_ia_related_content_tags_writing_post.md</code> in both French and English. Here is Claude's answer (again, I should have specified to "Stop being overly praiseworthy"):</p>

        <blockquote>
            The approach on Semantic Clustering is not only valid but forward-thinking. It correctly anticipates the SEO to GEO transition by creating a semantic clustering infrastructure that:
            <ul>
                <li>Maintains classic SEO compatibility</li>
                <li>Prepares the groundwork for GEO</li>
                <li>Facilitates migration from flat taxonomies to organic multilingual hierarchies</li>
                <li>Preserves human editorial validation</li>
            </ul>
            The risk identified (speed vs quality) is real and documented, but your end-to-end controlled editorial workflow protects you from drifting toward "slop". You're using AI as an efficiency amplifier, not as an automatic content generator.
            
            In strategic terms, you're positioning yourself exactly where you need to be in 2026: at the intersection of traditional SEO and emerging GEO, with tools that structure your content for machines while preserving editorial quality for humans.
        </blockquote>

        <h3>Information Risks in the Media Economic Model</h3>
        
        <p>I asked about information risks due to the collapse of the media economic model (see <code>034_ia_related_content_tags_writing_post.md</code>). This led deeper into a nightmare scenario based on:</p>
        <ul>
            <li>Paradox of ephemeral abundance</li>
            <li>Temporal compression effect of information</li>
            <li>Instant obsolescence syndrome</li>
            <li>Speed vs. truthfulness dilemma</li>
        </ul>
        
        <p>All of these lead to: (1) Speed Over Quality, (2) Fragmentation and Ephemerality, (3) Attention Economy!</p>

        <h3>Look & Feel: AI Output in the WordPress Theme</h3>
        
        <p>We all know that any functionality, even AI-powered, can fail if the UX and look-and-feel are poor. So I've reworked the output for both the breadcrumb and sidebar from the code output in the WordPress theme.</p>

        <h3>Using Docker to Test WordPress and the Plugin</h3>
        
        <p>As is often the case, a test environment is necessary to validate your plugin. Using Docker is a bit cumbersome, but also incredibly convenient, especially if you're injecting real production content into this development environment.</p>

        <pre>
# Commands for DOCKER

# Go to path
cd /Users/brunoflaven/Documents/01_work/blog_articles/_ia_augmented_journalist_wp_toolkit/ia_wp_plugin_related_content_steps/wp_docker

# Up docker
docker compose up -d

# Down docker
docker compose down
        </pre>

        <h3>Testing More Advanced Features (ENABLE LEVEL_2)</h3>
        
        <p>Creating a detailed plugin assessment involves describing the exact procedure of what you want to achieve as objectives in terms of business value, then assigning KPIs to reach these results. For example, I want the audience for the technical thematic tags (Python, Docker, AI, etc.) of my site to increase by 15% from English-speaking countries (USA, India).</p>

        <p><strong>It can definitely be improved, but the important thing is to capture the logic and principle: AI and Development are useless if there is no Business Value attached to them—otherwise you are heading nowhere.</strong></p>

        <ul>
            <li><strong>As a business requirement:</strong> The plugin assessment should include clear business objectives and KPIs. For example, increase the audience for technical tags (Python, Docker, AI) by 15% in English-speaking countries (USA, India) within 6 months, measured by unique page views.</li>
            <li><strong>As a user story:</strong> As a content strategist, I want to use [plugin/tool] to increase the audience for technical tags (Python, Docker, AI) by 15% in English-speaking countries (USA, India) within 6 months, so that we can grow our international user base.</li>
        </ul>

        <h3>Technical Validation Documentation</h3>
        
        <p>Do not hesitate to write precise documentation on how to check technical availability of the output.</p>

        <pre>
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

Fix any errors that appear (usually missing properties like image or publisher.logo).

Possible issues:
Issue 1: "Publisher logo is required"
Issue 2: "Image is required for Article"
Issue 3: Duplicate breadcrumbs from Yoast/RankMath
        </pre>

        <h3>Automation Philosophy</h3>
        
        <p>Try to automate as much as possible, especially time-consuming tasks that you will have to do repeatedly.</p>

        <p>This aligns with these principles:</p>
        <ol>
            <li>Automation of Repetitive Steps</li>
            <li>Time Savings</li>
            <li>Reusability</li>
            <li>Error Handling</li>
        </ol>

        <h4>Example: Database Import Script</h4>
        
        <pre>
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
        </pre>

        <h3>Motivation: Create a Motto</h3>
        
        <p>Forge a motto to motivate yourself. A quick, actionable insight on the 5D + Celebrate framework—tailored for your work as a writer, translator, and tech-savvy user:</p>

        <blockquote>
            Discuss, Design, Develop, Decide, DELIVER... and then celebrate.
        </blockquote>

        <h3>Documentation: Write for a Seven-Year-Old (As Persona)</h3>
        
        <p><strong>Think simple for your documentation—don't act like an expert! Here is some editorial advice:</strong></p>

        <ol>
            <li><strong>Tone & Style: Write Like a Story</strong>
                <ul>
                    <li>Narrative Flow: Treat it like a journal or case study—not a dry manual</li>
                    <li>Simple Language: Avoid jargon</li>
                    <li>Personal Touch: Add anecdotes</li>
                </ul>
            </li>
            <li><strong>Structure: Chronological + Practical</strong>
                <ul>
                    <li>Timeline (The "Story" Part)</li>
                    <li>Key Sections (The "How-To" Part)</li>
                </ul>
            </li>
        </ol>

        <h3>Plugin Blueprint: AI-Augmented Tagging</h3>
        
        <p>I am dealing with RELATED_TAGS or Tag Families. Here is a blueprint for the WordPress plugin that helps users pick the right tags for their blog posts, using AI and "named entities" (like people, places, or products mentioned in the text).</p>

        <blockquote>
            <strong>Objective:</strong> The AI-Augmented Tagging Plugin was created to automate and enhance the tagging process for WordPress blogs, leveraging Named Entity Recognition (NER) and semantic clustering. The goal was to save time, improve SEO, and ensure consistency across posts—especially for writers, translators, and content-heavy sites.
        </blockquote>

        <h4>CSV Structure for Tag Families</h4>

        <h5>Columns and Their Meanings</h5>
        <ul>
            <li><strong>family_id</strong> e.g., <code>0</code> – Family (cluster) ID</li>
            <li><strong>canonical_tag_id</strong> e.g., <code>6</code> – WordPress tag ID representing the family (the "parent")</li>
            <li><strong>canonical_label</strong> e.g., <code>information</code> – Name of the parent tag</li>
            <li><strong>tag_id</strong> e.g., <code>8</code> – ID of a family member (can be the parent or a child)</li>
            <li><strong>tag_label</strong> e.g., <code>infosuroit</code> – Name of the member tag</li>
            <li><strong>similarity_to_canonical</strong> e.g., <code>0.804</code> – Semantic similarity to the parent (0 to 1)</li>
            <li><strong>usage_count</strong> e.g., <code>5</code> – Number of posts using this tag</li>
            <li><strong>entity_label</strong> e.g., <code>O</code> – NER entity type (see table below)</li>
        </ul>

        <h5>Entity Types (entity_label)</h5>
        <ul>
            <li><strong>O</strong> – Outside (no special type) e.g., information, marketing, data</li>
            <li><strong>PERSON</strong> – Person e.g., jackson, robert jackson, susan jackson</li>
            <li><strong>ORG</strong> – Organization e.g., Adobe, 3WDOC, POC</li>
            <li><strong>GPE</strong> – Geopolitical entity e.g., Paris, France, New York</li>
            <li><strong>CARDINAL</strong> – Number e.g., 2012, 3, 100</li>
            <li><strong>DATE</strong> – Date e.g., January 2024, 2012</li>
            <li><strong>PRODUCT</strong> – Product e.g., Adsense, Photoshop</li>
        </ul>

        <h5>Key Rules</h5>
        <ol>
            <li>✅ Each family has <strong>ONLY ONE</strong> canonical_tag_id (the parent)</li>
            <li>✅ The canonical_label is <strong>IDENTICAL</strong> for all family members</li>
            <li>✅ The canonical tag appears as the first row (similarity = 1.0)</li>
            <li>✅ similarity_to_canonical: 1.0 = identical, &lt;1.0 = similar</li>
        </ol>

        <h3>Using Docker for Staging WordPress</h3>
        
        <pre>
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
        </pre>

        <h3>WordPress REST API Queries</h3>
        
        <p>To build effective AI applications, you need content—and ideally, structured content. The WordPress REST API provides exactly that. The idea is to fetch content directly from the API (either by calling it in real-time or downloading it as JSON files). Once you have the data, you can process it through your pipeline to perform semantic clustering—grouping related content based on meaning, not just keywords.</p>

        <pre>
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

# Examples:
# 10 most recent posts
https://your-site.com/wp-json/wp/v2/posts?per_page=10&page=1&orderby=date&order=desc

# First post ever published
https://your-site.com/wp-json/wp/v2/posts?per_page=1&orderby=date&order=asc

# Posts from 2025
https://your-site.com/wp-json/wp/v2/posts?after=2025-01-01T00:00:00&before=2026-01-01T00:00:00

# Posts 2020 to 2025 (dump into sample_posts_2020_to_2025.json)
https://your-site.com/wp-json/wp/v2/posts?after=2020-01-01T00:00:00&before=2026-01-01T00:00:00&per_page=100
        </pre>

        <h2>Using Mistral OCR</h2>
        
        <p>Create an environment and grab a production API key, then explore the documentation.</p>

        <pre>
# Install the environment
conda create -n mistral -y python=3.9
conda activate mistral
pip install mistralai python-dotenv datauri

# You need a PRODUCTION KEY for Mistral OCR
# Example: XXX-fake-mistral-ocr-api-key-7Df
        </pre>

        <p>Source: <a href="https://docs.mistral.ai/capabilities/document_ai/basic_ocr" target="_blank" rel="noopener">https://docs.mistral.ai/capabilities/document_ai/basic_ocr</a></p>

        <h2>Challenges in Training Whisper for Custom Languages</h2>

        <h3>The Linguistic Landscape: Key African Languages</h3>
        
        <p>Africa is home to a vast array of languages, many of which are widely spoken but underrepresented in speech recognition technologies. Some of the most prominent include:</p>

        <table>
            <thead>
                <tr>
                    <th>Language</th>
                    <th>Speakers (approx.)</th>
                    <th>Regions & Diaspora</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Yoruba</td>
                    <td>30 million</td>
                    <td>Nigeria, Benin, Togo</td>
                </tr>
                <tr>
                    <td>Oromo</td>
                    <td>30 million</td>
                    <td>Ethiopia</td>
                </tr>
                <tr>
                    <td>Igbo</td>
                    <td>24 million</td>
                    <td>Nigeria</td>
                </tr>
                <tr>
                    <td>Zulu (isiZulu)</td>
                    <td>12 million</td>
                    <td>South Africa</td>
                </tr>
                <tr>
                    <td>Lingala</td>
                    <td>10 million</td>
                    <td>DRC, Republic of Congo</td>
                </tr>
                <tr>
                    <td>Wolof</td>
                    <td>9.4 million</td>
                    <td>Senegal (85% of population)</td>
                </tr>
                <tr>
                    <td>Somali</td>
                    <td>28 million</td>
                    <td>Somalia, Somaliland, Djibouti, Ethiopia, Kenya</td>
                </tr>
                <tr>
                    <td>Kirundi</td>
                    <td>12 million</td>
                    <td>Burundi, Rwanda, Tanzania, DRC, Uganda</td>
                </tr>
                <tr>
                    <td>Amharic</td>
                    <td>10 million</td>
                    <td>Ethiopia</td>
                </tr>
                <tr>
                    <td>Tigrinya</td>
                    <td>1.6 million</td>
                    <td>Eritrea (50% of population)</td>
                </tr>
            </tbody>
        </table>

        <p>These languages, while rich and diverse, pose significant challenges for speech recognition models due to limited training data and dialectal variations.</p>

        <h3>Case Studies: The Challenges of Multilingual Speech Recognition</h3>

        <h4>1. Tunisian Dialect (DJO Project)</h4>
        <ul>
            <li><strong>Problem:</strong> Tunisian Arabic is a dialectal variant of Arabic, distinct from Modern Standard Arabic (MSA). Existing models like Whisper struggle to accurately transcribe Tunisian due to its unique vocabulary, pronunciation, and lack of standardized written form.</li>
            <li><strong>Solution:</strong> The AI platform "<a href="https://akademie.dw.com/en/an-ai-platform-wins-top-2025-media-loves-tech-prize/a-75134414" target="_blank" rel="noopener">DJO</a>", winner of the 2025 Media Loves Tech Grand Prize, was developed to address this gap. It focuses on improving transcription accuracy for Tunisian Arabic by leveraging localized datasets and fine-tuning Whisper.</li>
        </ul>

        <h4>2. Senegalese Languages (Wolof, Diola, Fulfude)</h4>
        
        <p>Thanks to Codou for the explanations!</p>

        <ul>
            <li><strong>Problem:</strong> In Senegal, multilingualism is common, with Wolof, Diola, and Fulfude (Peul) spoken alongside French and English. Whisper and other models often fail to distinguish between these languages or accurately transcribe them, especially in code-switching scenarios (mixing languages in a single sentence).</li>
            <li><strong>Impact:</strong> Poor transcription quality limits the usability of voice-based applications, such as chatbots or media subtitling, for local populations.</li>
        </ul>

        <h4>3. Multilingual Challenges (Mandenkan, Fulfude, Hausa, Kiswahili)</h4>
        <ul>
            <li><strong>Problem:</strong> International media (e.g., radio, television) broadcast in multiple African languages, including Mandenkan, Fulfude, Hausa, and Kiswahili. Whisper's performance is inconsistent across these languages, particularly for named entities (e.g., proper nouns, locations).</li>
            <li><strong>Root Cause:</strong> The lack of high-quality, language-specific training data and the complexity of dialectal variations.</li>
        </ul>

        <h3>Technical Insights: Testing Whisper and Alternatives</h3>

        <h4>Test Results Summary</h4>
        
        <p>I conducted several tests:</p>
        <ul>
            <li><strong>Whisper Large, Custom Implementation:</strong> Achieved the best transcription results among the tested models.</li>
            <li><strong>MMS by Facebook AI:</strong> Despite supporting over 1,000 languages (including Swahili), the transcription quality was disappointing.</li>
            <li><strong>Fine-tuned Whisper Large & Small:</strong> Both performed poorly, likely due to insufficient training data or suboptimal fine-tuning processes.</li>
        </ul>

        <h4>Key Observations</h4>
        <ul>
            <li><strong>Training Complexity:</strong> Fine-tuning Whisper for low-resource languages is technically demanding. Success depends on the quality and quantity of the training corpus.</li>
            <li><strong>Named Entity Recognition:</strong> Even with a robust transcription model, poor transcription quality undermines named entity recognition. For example, "Pape Gueye" was incorrectly transcribed as "Pape Gay"—a common issue when dealing with proper nouns in underrepresented languages.</li>
            <li><strong>Post-Processing Limitations:</strong> While post-processing can improve results, it cannot fully compensate for fundamental transcription errors.</li>
        </ul>

        <h3>Conclusion: The Path Forward</h3>

        <h4>Immediate Solution</h4>
        <ul>
            <li><strong>Status Quo:</strong> Continue using Whisper Large with the current implementation, supplemented by post-processing where possible.</li>
        </ul>

        <h4>Long-Term Goal</h4>
        <ul>
            <li><strong>Custom Training:</strong> Train Whisper Large on domain-specific datasets (e.g., Swahili content) to significantly improve transcription accuracy. This approach has proven successful for French, as demonstrated by Radio France's use of specific datasets.</li>
            <li><strong>Named Entity Improvement:</strong> Refine the list of named entities (tags) for better editorial accuracy, though transcription quality remains the primary bottleneck.</li>
        </ul>

        <h4>Final Thought</h4>
        <p>Without access to better models or the ability to train on dedicated, high-quality datasets, the current implementation of Whisper Large remains the most viable option. However, the ultimate goal is to bridge the gap for African and dialectal languages through targeted training and community-driven data collection.</p>
    </article>
</body>
</html>
```


## PROMPT_2
As editorial editor in english, can you correct and refine this text below, at least reoganise the ideas so it is readable.
Print as HTML.



```html
<H3>Words have meaning</H3>

Why did I become interested in the quality of transcriptions on whisper and the problem of "neglected" languages, particularly Arabic or African languages?

Because professionally I have to manage some of these languages, and not everyone is going to end up speaking English. Technological dominance is one thing, cultural dominance is one another.

So, professionally, I became interested in the following languages: Mandinka, Fulfulde, Hausa, and Swahili.

Thanks also to Codou Ndiaye and the two creators of the DJO project, I became interested in Wolof and Tunisian Arabic.

DJO is an AI-powered software project for Tunisian-language journalists, Fares Mallouli Mallouli and Mohamed Amine Macherki, winners of the Deutsche Welle MEDIA LOVES TECH Grand Prize.

Source : <a href=" https://akademie.dw.com/en/an-ai-platform-wins-top-2025-media-loves-tech-prize/a-75134414" target="_blank" rel="noopener"> https://akademie.dw.com/en/an-ai-platform-wins-top-2025-media-loves-tech-prize/a-75134414</a>

I have worked with Codou Ndiaye on two subjects; using IA for the Wolof, conducting IA's experiments to use for customer support. Two vast and interesting topics.

With the DJO founders, I discussed this project for the automatic transcription of the Tunisian dialect, detailing the challenges of multilingualism, data collection, and the technical specificities related to code-switching.

DJO trained Whisper to improve its transcription performance for the three languages that make up Tunisian Arabic: English, French, and the Tunisian dialect. According to Codou Ndiaye, in Senegal, the same operation should be carried out using Whisper for transcription, but with a larger number of language combinations. Multilingualism is much more widespread in Africa, and its corollary, code-switching, is a key factor. The population often speaks two or three languages in addition to one or even two European languages.


<b>According to Codou Ndiaye, the code-switching in Senegal.</b>
<ul>
<li>English, French, and Wolof</li>
<li>English, French, and Diola</li>
<li>English, French, and Fulfulde or Peul</li>
</ul>

In any case, it's a prerequisite if you want to offer transcription services to journalists or a customer support chatbot, for example, in the language of a country like Senegal or Tunisia.

Moreover, building models specifically trained for the local market and its speakers is a mark of sovereignty and digital independence.

During these discussions, like I said before, I discovered that this language switching is called code-switching. It's quite characteristic of Wolof, Tunisian Arabic, and other African languages.

<blockquote>Code-switching is the alternation between several linguistic codes (languages, dialects, or language registers) within a single discourse or utterance, or even within a sentence, most often where the syntax of the two codes aligns.</blockquote>

Source: More on Code-switching <a href="https://en.wikipedia.org/wiki/Code-switching" target="_blank" rel="noopener">https://en.wikipedia.org/wiki/Code-switching</a>

It seems likely that this approach should also be applied to the other most widely spoken African languages: Yoruba, Oromo, Igbo, Zulu, Lingala, Somali, Kirundi, Amharic, Tigrinya, etc.

The eagerness of the GAFA companies (Meta, OpenAI, Google, Anthropo, Amazon, Apple, etc.), mostly American and therefore English-speaking, to take an interest in these languages is undoubtedly quite limited! Whose fault is it? The lack of resources in the language to train a model, the lack of available speakers to correct inferences, the hypothetical financial interest proportional to the investment, and increasingly aggressive American diplomacy... At the same time, Africa is the object of intense interest from the three major powers of the moment: the USA, Russia, and China. It could give a small boost to their soft power if one of these powers were to offer models adapted to local languages.

Language is, after all, the essential vehicle for many things (culture, discourse, politics, information). Words have meaning, and their precision in transcription, for example, is paramount.

At the risk of sounding condescending, linguistic poverty is often a sign of profound intellectual poverty. I'm not pointing fingers.

<b>"The limits of my language are the limits of my world."</b> Ludwig Wittgenstein

I know, I know, I have a friend who tells me I intellectualize everything, and she's absolutely right!

The danger of disintermediation, combined with cultural and technological dominance, lies in the fact that the fragmentation of demand weakens you as an individual or group of individuals in the face of a supply that naturally tends to concentrate. (See the platformization of AI supply; basically, the game is rigged between the GAFAM companies.)

Thus, if you represent a small fraction of humanity —for example, if you are a speaker of a rare language or part of a group of speakers—well, there is little chance that you will be served, or even not served at all, because you represent a negligible quantity in terms of market share. This is the harsh reality of the market. All that remains is for you to take control of your destiny by training your LLM (Language, Language, and Media) and thus seizing power and sovereignty. This is mainly the cause of my practice.
```


## OUTPUT_2
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Words Have Meaning</title>
</head>
<body>
    <article>
        <h3>Words Have Meaning</h3>
        
        <h4>Why Transcription Quality Matters for Underserved Languages</h4>
        <p>Why did I become interested in the quality of transcriptions on Whisper and the problem of "neglected" languages, particularly Arabic and African languages?</p>
        
        <p>The answer is professional necessity. I manage content in several of these languages, and not everyone is going to end up speaking English. Technological dominance is one thing; cultural dominance is another entirely.</p>
        
        <h4>Languages and Collaborations</h4>
        <p>Professionally, I work with the following languages: Mandinka, Fulfulde, Hausa, and Swahili.</p>
        
        <p>Thanks to Codou Ndiaye and the creators of the DJO project—Fares Mallouli and Mohamed Amine Macherki, winners of the Deutsche Welle MEDIA LOVES TECH Grand Prize—I also became interested in Wolof and Tunisian Arabic.</p>
        
        <p>DJO is an AI-powered software project for Tunisian-language journalists. Source: <a href="https://akademie.dw.com/en/an-ai-platform-wins-top-2025-media-loves-tech-prize/a-75134414" target="_blank" rel="noopener">https://akademie.dw.com/en/an-ai-platform-wins-top-2025-media-loves-tech-prize/a-75134414</a></p>
        
        <p>I have collaborated with Codou Ndiaye on two subjects: using AI for Wolof, and conducting experiments with AI for customer support. Both are vast and fascinating topics.</p>
        
        <p>With the DJO founders, I discussed their project for automatic transcription of the Tunisian dialect, exploring the challenges of multilingualism, data collection, and the technical specificities related to code-switching.</p>
        
        <h4>Understanding Code-Switching</h4>
        <p>DJO trained Whisper to improve its transcription performance for the three languages that comprise Tunisian Arabic: English, French, and the Tunisian dialect. According to Codou Ndiaye, the same operation should be carried out in Senegal, but with an even larger number of language combinations. Multilingualism is far more widespread in Africa, and its corollary—code-switching—is a critical factor. The population often speaks two or three local languages in addition to one or even two European languages.</p>
        
        <p><strong>According to Codou Ndiaye, common code-switching patterns in Senegal include:</strong></p>
        <ul>
            <li>English, French, and Wolof</li>
            <li>English, French, and Diola</li>
            <li>English, French, and Fulfulde (Peul)</li>
        </ul>
        
        <p>Understanding and accommodating code-switching is a prerequisite for offering transcription services to journalists or customer support chatbots in countries like Senegal or Tunisia.</p>
        
        <blockquote>Code-switching is the alternation between several linguistic codes (languages, dialects, or language registers) within a single discourse or utterance, or even within a sentence, most often where the syntax of the two codes aligns.</blockquote>
        
        <p>Source: <a href="https://en.wikipedia.org/wiki/Code-switching" target="_blank" rel="noopener">https://en.wikipedia.org/wiki/Code-switching</a></p>
        
        <p>This approach should likely be applied to other widely spoken African languages: Yoruba, Oromo, Igbo, Zulu, Lingala, Somali, Kirundi, Amharic, Tigrinya, and others.</p>
        
        <h4>Digital Sovereignty and Independence</h4>
        <p>Building models specifically trained for local markets and their speakers is a mark of sovereignty and digital independence. This is not merely a technical consideration—it's a political and cultural imperative.</p>
        
        <h4>The GAFA Gap</h4>
        <p>The eagerness of major tech companies (Meta, OpenAI, Google, Anthropic, Amazon, Apple, etc.)—mostly American and therefore English-speaking—to invest in these languages is undoubtedly quite limited. Whose fault is it? Multiple factors contribute:</p>
        <ul>
            <li>Lack of language resources to train models</li>
            <li>Lack of available speakers to correct inferences</li>
            <li>Questionable financial returns proportional to investment</li>
            <li>Increasingly aggressive American diplomacy</li>
        </ul>
        
        <p>Meanwhile, Africa is the object of intense interest from three major powers: the USA, Russia, and China. Offering models adapted to local languages could provide a significant soft power advantage to whichever nation takes the initiative.</p>
        
        <h4>The Power of Language</h4>
        <p>Language is, after all, the essential vehicle for many things: culture, discourse, politics, information. Words have meaning, and their precision in transcription is paramount.</p>
        
        <p>At the risk of sounding condescending, linguistic poverty is often a sign of profound intellectual poverty. I'm not pointing fingers—I'm stating a reality.</p>
        
        <p><strong>"The limits of my language are the limits of my world."</strong> — Ludwig Wittgenstein</p>
        
        <p>I know, I know—a friend tells me I intellectualize everything, and she's absolutely right!</p>
        
        <h4>Market Dynamics and Self-Determination</h4>
        <p>The danger of disintermediation, combined with cultural and technological dominance, lies in the fact that fragmented demand weakens you as an individual or group of individuals in the face of supply that naturally tends to concentrate. (See the platformization of AI supply—basically, the game is rigged in favor of the GAFAM companies.)</p>
        
        <p>Thus, if you represent a small fraction of humanity—for example, if you speak a rare language or belong to a minority linguistic community—there is little chance you will be served well, or perhaps not served at all, because you represent a negligible market share. This is the harsh reality of the market.</p>
        
        <p>What remains is to take control of your destiny by training your own LLM (Large Language Model) and thus seizing power and sovereignty. This is the driving force behind my practice.</p>
    </article>
</body>
</html>
```
## OUTPUT_1
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Will Kill Almost All Work Ethics</title>
</head>
<body>
    <article>
        <h3>AI Will Kill Almost All Work Ethics</h3>
        
        <h4>On Silence and Absence</h4>
        <p>It's been ages since I've written anything or posted a video on YouTube. My online presence is abysmal. Is this the beginning of the wisdom of keeping quiet when you have nothing to say, or is it merely another manifestation of what I call Digital January Diet (DJD)?</p>
        
        <p>This raises a fundamental question: Why blame myself and see this prolonged absence as a disadvantage? Isn't it said that distance creates power? Why not approach the problem from the opposite angle and finally celebrate frugality in a society of abundance—where everyone feels compelled to have something to say about everything, including AI?</p>
        
        <h4>The Virtue of Restraint</h4>
        <p>Can't we opt for a more reasonable and virtuous counterpoint? Consider these opposing forces:</p>
        <ul>
            <li>Gluttony vs. Frugality</li>
            <li>Debauchery vs. Abstinence</li>
            <li>Lies vs. Truth</li>
            <li>Dependence vs. Sovereignty</li>
            <li>...the list goes on</li>
        </ul>
        
        <p>I'll let you guess where I stand between these rather black-and-white positions.</p>
        
        <h4>The Paradox I Embody</h4>
        <p>My characteristic mild cynicism tells me that claiming to be on one side or the other is just posturing. I know this all too well: I advocate for the responsible use of AI yet abuse it whenever possible. I express concern about LLM sovereignty while using American or Chinese models all day long. The contradictions are glaring.</p>
        
        <h4>The Backlog</h4>
        <p>But let me get to the point. I mainly want to wrap up some topics I've been working on so I can move forward. My Mac is overflowing with Proofs of Concept (POCs), trial-and-error experiments, and unfinished projects. There's been a lull in my publishing schedule—much like when dishes pile up in the sink or laundry accumulates, and you finally have to deal with it.</p>
        
        <p>Specifically, I'm exploring technical AI topics for personal projects, inventing and creating while earning a salary for doing very little—or at least avoiding the most challenging work.</p>
        
        <h4>The Fear of Imperfection</h4>
        <p>I'm still hesitant to publish all my trial-and-error work: the adjustments, the sometimes botched workarounds, the risky guesswork, or simply anything that reveals my ignorance. Yet recognizing one's ignorance is the first step in learning.</p>
        
        <h4>AI's Revolutionary Impact</h4>
        <p>It must be acknowledged that AI is sweeping everything away: posture, knowledge, hierarchical functions—literally everything. Nothing seems to resist it: not advice, not training, not technical skills. It's reminiscent of the French revolutionary slogan of 1789: "Liberty or death"—except now it's "AI or death."</p>
        
        <h4>Publishing Prompts: A Record of Cognitive Process</h4>
        <p>My approach moving forward is to publish all my prompts. They serve as a record of my cognitive process—"step by step," or perhaps more accurately, "error by error."</p>
        
        <p>By publishing my prompts, you'll also see that I'm increasingly suffering from intellectual laziness, especially when it comes to writing code. I would be utterly unable to produce even a quarter of what I now create without AI assistance, including presentations.</p>
        
        <p>For transparency: this code was primarily written by Claude and Perplexity.</p>
    </article>
</body>
</html>
```