seo_prompts={

### SEO WORKSHOP
"seo_manage_title" : """ 
As an SEO expert proficient, could you create 10 compelling headline ideas for a post about {user_input} in the same language as the post? 
""",

"seo_manage_url" : """ 
As an SEO expert proficient, create 10 compelling URL ideas for a post about {user_input} in the same language as the post? 
""",

"seo_manage_meta_description" : """ 
As an SEO expert proficient, please write a meta description of 150-160 characters for a post about {user_input} in the same language as the post. 
""",

"seo_manage_label_internal_link" : """ 
As an SEO expert proficient, please generate 10 semantic editorial proposals for link labels based on a post about {user_input} in the same language as the post. 
""",

"seo_manage_ner_tags" : """ 
Given the input text:user input: {user_input} perform NER detection on it. NER TAGS: FAC;  CARDINAL;  NUMBER;  DEMONYM;  QUANTITY;  TITLE;  PHONE_NUMBER;  NATIONAL;  JOB;  PERSON;  LOC;  NORP;  TIME;  CITY;  EMAIL;  GPE;  LANGUAGE;  PRODUCT;  ZIP_CODE;  ADDRESS;  MONEY;  ORDINAL;  DATE;  EVENT;  CRIMINAL_CHARGE;  STATE_OR_PROVINCE;  RELIGION;  DURATION;  WORK_OF_ART;  PERCENT;  CAUSE_OF_DEATH;  COUNTRY;  ORG;  LAW;  NAME;  COUNTRY;  RELIGION;  TIME answer must be in the format tag:value 
""",

"seo_manage_html_subtitles" : """ 
As an SEO expert proficient,  please generate an HTML code structure for the post content: "{user_input}" in the same language as the post. Use <H1>, <H2>, and <H3> tags to organize the content effectively. Ensure the structure follows best SEO practices for optimal readability and search engine optimization. 
""",

"seo_manage_image_alt_attribute" : """ 
As an SEO expert proficient, please generate 10 alt text descriptions for images related to the main topic of the post: "{user_input}" in the same language as the post. Each alt text should incorporate synonyms or variations of the main keyword and must not exceed 125 characters. 
"""

### OTHER SEO PROMPTS

### 1. Conduct Keyword Research 
"seo_other_conduct_keyword_research" = """ 
As a SEO expert, can you help me identify high-volume and low-competition keywords for a post about '{user_input}' in the same language as the post? Please provide a list of 10 keywords along with their search volume and competition level?
"""

### 2. Group Keywords Based on Semantic Relevance
"seo_other_group_keywords_semantic_relevance" = """
As a SEO expert, I have a list of keywords related to '{user_input}'. Can you define a list of keywords in the same language as the post and group these keywords into categories based on their semantic relevance in the same language as the post?.
"""

### 3. Create Topic Clusters
"seo_other_create_topic_clusters" = """
As a SEO expert, I want to create topic clusters for my post about '{user_input}'. Can you suggest main topics and subtopics that would form effective content clusters in the same language as the post??
 """

### 4. Generate Headline Ideas
"seo_other_generate_headline_ideas" = """
As a SEO expert, can you generate 10 compelling headline ideas for a post about '{user_input}' in the same language as the post?
"""

### 5. Craft Content Outlines
"seo_other_craft_content_outlines" = """
As a SEO expert, I need an outline for a blog post titled '{user_input}' in the same language as the post. Can you provide a detailed outline including introduction, main points, and conclusion in the same language as the post?
"""

### 6. Create Content
"seo_other_create_content" = """
As a SEO expert, can you write a 500-word post about '{user_input}' in the same language as the post? Please make it engaging and SEO-friendly.
"""

### 7. Identify Websites for Guest Post Outreach
"seo_other_identify_websites_guest_post_outreach" = """
As a SEO expert, can you help me identify 10 high-authority websites, in the same language as the post, where I can submit a guest post about '{user_input}'? Please include their domain authority and contact information if available.
"""

### 8. Generate Structured Data
"seo_other_generate_structured_data" = """
As a SEO expert, can you generate structured data (schema markup) for an article about '{user_input}'? in the same language as the post? Please provide the JSON-LD format.
"""

### 9. Automate Meta Description Writing
"seo_other_automate_meta_description_writing" = """
As a SEO expert, I need meta descriptions for my website pages about '{user_input}' in the same language as the pages?. Can you generate unique meta descriptions for each of these pages in the same language as the pages?
"""

### 10. Write Meta Tags
"seo_other_write_meta_tags" = """
As a SEO expert, can you help me write meta tags for a post about '{user_input}' in the same language as the post? Please include title tags and meta descriptions.
"""

### 11. Create Crawl Directives for Robots.txt
"seo_other_create_crawl_directives_robots" = """
As a SEO expert, I need to create a robots.txt file for my website. Can you generate directives to allow all search engines to crawl the site but disallow them from indexing the '{user_input}' directory?
"""

### 12. Create Regular Expression (Regex) Patterns
"seo_other_create_regex_patterns" = """
As a SEO expert, can you provide a regex pattern to match all '{user_input}' in a text? Also, explain how this pattern works.
"""

### 13. Generate Sitemaps
"seo_other_generate_sitemaps" = """
As a SEO expert, can you help me generate an XML sitemap for a website with the following URLs: '{user_input}' ? Please include the priority and change frequency for each URL.
"""

}

"""
### 1. Conduct Keyword Research
**Prompt**:
```bash 
ChatGPT, can you help me identify high-volume and low-competition keywords for a blog about 'healthy eating habits'? Please provide a list of 10 keywords along with their search volume and competition level.
```
### 2. Group Keywords Based on Semantic Relevance
**Prompt**: 
```bash
ChatGPT, I have a list of keywords related to 'digital marketing'. Can you group these keywords into categories based on their semantic relevance? Here is the list: SEO, social media marketing, content marketing, email marketing, PPC advertising.
```
### 3. Create Topic Clusters
**Prompt**: 
```bash
ChatGPT, I want to create topic clusters for my blog about 'personal finance'. Can you suggest main topics and subtopics that would form effective content clusters?
```

### 4. Generate Headline Ideas
**Prompt**: 
```bash
ChatGPT, can you generate 10 compelling headline ideas for a blog post about 'the benefits of yoga for mental health'?
```

### 5. Craft Content Outlines
**Prompt**: 
```bash ChatGPT, I need an outline for a blog post titled 'The Ultimate Guide to Remote Work'. Can you provide a detailed outline including introduction, main points, and conclusion?
```

### 6. Create Content
**Prompt**: 
```bash
ChatGPT, can you write a 500-word blog post about 'how to create a morning routine that boosts productivity'? Please make it engaging and SEO-friendly.
```

### 7. Identify Websites for Guest Post Outreach
**Prompt**: 
```bash
ChatGPT, can you help me identify 10 high-authority websites where I can submit a guest post about 'sustainable living'? Please include their domain authority and contact information if available.
```

### 8. Generate Structured Data
**Prompt**: 
```bash
ChatGPT, can you generate structured data (schema markup) for an article about 'the best vegan recipes'? Please provide the JSON-LD format.
```

### 9. Automate Meta Description Writing
**Prompt**: 
```bash
ChatGPT, I need meta descriptions for my website pages about 'digital marketing services'. Can you generate unique meta descriptions for each of these pages: SEO, PPC, content marketing, social media marketing?
```

### 10. Write Meta Tags
**Prompt**: 
```bash
ChatGPT, can you help me write meta tags for a webpage about 'eco-friendly home improvements'? Please include title tags and meta descriptions.
```

### 11. Create Crawl Directives for Robots.txt
**Prompt**: 
```bash
ChatGPT, I need to create a robots.txt file for my website. Can you generate directives to allow all search engines to crawl the site but disallow them from indexing the 'private' directory?
```

### 12. Create Regular Expression (Regex) Patterns
**Prompt**: 
```bash
ChatGPT, can you provide a regex pattern to match all email addresses in a text? Also, explain how this pattern works.
```

### 13. Generate Sitemaps
**Prompt**: 
```bash
ChatGPT, can you help me generate an XML sitemap for a website with the following URLs: /home, /about, /services, /blog, /contact? Please include the priority and change frequency for each URL.
```
"""
