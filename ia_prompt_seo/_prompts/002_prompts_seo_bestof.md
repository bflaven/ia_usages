# 002_prompts_seo_bestof.md


## seo_manage_title


SEO's most valuable variable: the content's title or headline


```bash
As an SEO expert, can you generate 10 compelling headline ideas for a post about "the benefits of yoga for mental health"?
```

**Friendly fire...**
```bash
Hey ChatGPT, tell me....
```

**What is a good "SEO" title?**

- Unique title, descriptive, short, concise and makes you want to click
- The main keyword ie on the subject of the subject at the beginning of the title
- The title must be between 51 to 60 characters

Objective: Creative exercise because you have to ask yourself what is the main subject or the two main subjects of a piece of content that your are about to write.



**SEO tools for title management**
- https://moz.com/learn/seo/title-tag
- https://technicalseo.com/tools/google-serp-simulator/


**Code**
- https://github.com/ViniciusStanula/seo-bulk-gpt-meta-tags-creator/tree/main
- https://github.com/BanukaSEO/SEO_H1_and_Title_Generator/tree/main
- https://github.com/patrickfearon/serpsim


## seo_manage_url

SEO's most valuable variable: the content's url or slug


```bash
As an SEO expert, can you generate 10 compelling url ideas for a post about "the benefits of yoga for mental health"?
```


**What is a good "SEO" url?**
- Descriptive URL, short, concise and makes you want to click
- As for the title, main keywords at the beginning
- Special characters and accents to avoid
- Do not modify the URL of the post once published unless necessary

**Objective: Very strong correlation between title and URL**

## seo_manage_meta_description

```bash
As an SEO expert, write a meta description of 150-160 characters for a blog post on "Effective link-building strategies."

```

**What is a good "SEO" Meta description?**
- The meta description is important because it gives a description to the content
- It helps to encourage clicks from the SERP (Search Engine Result Page)
- It must be short to be readable for people.
- It must be between 150 and 160 characters long.


## seo_manage_backlink_internal_links


There are two types of links:
- backlink or inbound link (link to content from another domain site A to site B)
- internal link (link to content on the same domain site A to site A)


## seo_manage_external_linking

- external linking (inbound link): practice that increases relevance and curation

Points of vigilance: do not make too many outgoing links, do not make links to non-quality sites.

External linking involves the creation of inbound links (backlinks) from other websites.

**Link building is another fundamental aspect of SEO. By obtaining inbound links from other websites, you can improve your website's authority, visibility, and ranking in search engine results. Chat GPT can help streamline the link building process by providing you with a complete list of websites to utilize for your off-page strategy.**

**10 Prompts to Build Backlinks with AI**

Here are 10 easy ways to use Chat GPT to build backlinks:

```bash
# PROMPT_1
Give a list of article submission and guest posting websites for your niche: These are links embedded in an article or blog post that often come from guest posts where you write content for another website and include a link to your site in the author bio or body of the post.

# PROMPT_2
Give a list of profile creation websites for your niche: These are links on your social media or professional profiles, such as LinkedIn or Twitter. They are very easy to create - you only need to add the business name, your website URL, the business description/bio, and the tags.

# PROMPT_3
Give a list of social bookmarking websites for your niche: These are links to your site saved by users on social bookmarking sites such as Reddit, Digg, and Delicious.

# PROMPT_4
Give a list of directory websites for your niche: These are links from web directories such as Yellow Pages or Yelp.

# PROMPT_5
Give a list of Wiki-like websites for your niche: These are links from Wikipedia or other wikis. They are valuable because they come from an authoritative source, but they can be hard to obtain.

# PROMPT_6
Give a list of forum websites for your niche: These are links from online forums such as Reddit or Quora. These links can be valuable if they come from a relevant and authoritative source.

# PROMPT_7
Give a list of document sharing websites for your niche: These are links from sharing documents such as PDFs or PowerPoint presentations on sites like SlideShare or Scribd.

# PROMPT_8
Give a list of image sharing websites for your niche: These are links from sharing images on sites such as Pinterest or Flickr.

# PROMPT_9
Give a list of Web 2.0 websites for your niche: These are links from Web 2.0 sites such as blogger or WordPress.com, where you can create a free blog and include links to your site.

# PROMPT_10
Give a list of press release websites for your niche: Press release for off-page SEO is a practice of writing newsworthy press releases and distributing them to journalists and media to get quality links to your website.
```

## seo_manage_internal_linking
- It helps to stimulate the relevance of an article on a subject
- It allows the user to discover other content from site A (retention)
- It allows spiders to track the depth of content on site A
makes content more editorially attractive

**Internal linking in SEO connects the pages of the same site.**

## seo_manage_label_internal_link

This is the label on which the user will click to access the link.

- preferably, you need a keyword on the main subject of the target URL
- the label must be descriptive of the link but avoiding general words (here, more details, announced, declared....etc)
- make a descriptive label which demonstrates the editorial content of the target link
- 



## seo_manage_ner_tags

- Try to make a link on each named entities e.g. Person, Country, City, Event... from an post to the respective tag pages using direct link. It is highly connected ot the NLP NER concept. 

- Try to make a direct link to one or several page according to your main navigation or taxonomy e.g WP categories. You can the pormpt or th LLM to force CATEGORIZATION according to the content of the post.

*Caution: Do not necessarily be systematic and do not force on these linking types. This is savy both in AI or in SEO.**



## seo_manage_reverse_linking

1. I have just published an post_1 on a SUBJECT
2. I will search for the last 5 posts on the SUBJECT (post_2, post_3... etc)
3. I will modify the last 5 articles on the same SUBJECT (post_2, post_3... etc) by adding a link to post_1

BONUS: take out the top 5 latest articles from the point of view of SEO traffic on the same SUBJECT and insert a link to the post_1


**Why you should reverse linking?**
The idea is to "force" Google, which has already discovered the previous posts which are therefore popular, to discover the new post. This is a transfer of popularity from previous posts to the new post.



As an SEO expert, here is my workflow for boosting the visibility of a newly published post:

1. **Publish New Content**: I have just published a new post, **post_1**, on a specific SUBJECT.
2. **Identify Recent Posts**: I will search for the last 5 posts (post_2, post_3, post_4, post_5, post_6) on the same SUBJECT.
3. **Update Previous Posts**: I will modify these last 5 articles by adding a link to **post_1**.

**Bonus Task**: Identify the top 5 articles with the highest SEO traffic on the same SUBJECT and insert a link to **post_1** in each of them.

**Objective**: The goal is to leverage the popularity of previously discovered and popular posts to help Google discover and index the new post quickly. This technique transfers SEO authority and traffic from the older posts to the new post, enhancing its visibility and search engine ranking.



## seo_manage_html_subtitles


```bash
As an SEO expert, can you generate an HTML code structure using `<H1>`, `<H2>`, and `<H3>` tags for the post content provided below? Please ensure that the code adheres to best SEO practices for optimal content structure, readability, and search engine optimization.
```

```bash
As an SEO expert, I would like you to generate an optimized HTML code structure for the post content provided below. The HTML code should be well-structured and follow best SEO practices to ensure that the content is easily crawlable and indexable by search engines.

Specifically, you should use header tags (H1, H2, H3) to accurately reflect the hierarchy and importance of the content. The H1 tag should be used for the main title of the post, while the H2 and H3 tags should be used for subheadings and sub-subheadings, respectively.

In addition to the header tags, the HTML code should also include other relevant on-page SEO elements, such as a meta title and meta description. The meta title should be concise and accurately reflect the main topic of the post, while the meta description should provide a brief summary of the post's content and entice users to click through to the post.

Finally, the HTML code should be easy to read and understand, with proper indentation and comments where necessary. The resulting HTML code should be ready for implementation on the website, with all necessary elements included and optimized for SEO.
```

**What is a good "SEO" structure for HTML?**

Structure the content using subtitles (H1, H2, H3, etc.) to prioritize the information contained in the article.

**HowTo structure for HTML or "what to put in the subtitles
"?**
- main keywords of the article
- questions that audiences might have on the subject
- related search from trends

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>The Benefits of Yoga for Mental Health</title>
  <meta name="description" content="Discover the many benefits of yoga for mental health, including reduced stress and anxiety, improved mood, and increased self-awareness.">
</head>
<body>
  <article>
    <header>
      <h1>The Benefits of Yoga for Mental Health</h1>
    </header>
    <section>
      <h2>Reduced Stress and Anxiety</h2>
      <p>Practicing yoga can help reduce the levels of cortisol, the stress hormone, in the body. It can also activate the relaxation response, which can help alleviate symptoms of anxiety.</p>
    </section>
    <section>
      <h2>Improved Mood</h2>
      <p>Yoga has been shown to increase the production of feel-good chemicals in the brain, such as endorphins and GABA, which can help improve mood and reduce symptoms of depression.</p>
    </section>
    <section>
      <h2>Increased Self-Awareness</h2>
      <p>Through the practice of mindfulness and meditation, yoga can help increase self-awareness and promote a greater sense of self-acceptance and compassion.</p>
    </section>
    <section>
      <h3>How to Get Started with Yoga</h3>
      <p>If you're new to yoga, consider starting with a beginner's class or an online tutorial. It's important to listen to your body and modify poses as needed to avoid injury.</p>
    </section>
  </article>
</body>
</html>
```


## seo_manage_image_optimization

- Select an original photo is 100 times better than an already used image.
- image filename must be human-readable, it helps with SEO


```bash


# YEP
https://flaven.fr/wp-content/uploads/2024/04/ia_building_llm_api_web_apps_start_finish_b_2.png


# NOPE
https://flaven.fr/wp-content/uploads/2024/04/img_120508_171442.png



```

## seo_manage_image_alt_attribute

- describe the image clearly, specifically
- image type
- if the photo contains text, this must be specified in the alt message
- describe the image as if presenting it to someone
- concise do not exceed 125 characters

BONUS: Use synonyms or variations of the main keyword from the post. 


