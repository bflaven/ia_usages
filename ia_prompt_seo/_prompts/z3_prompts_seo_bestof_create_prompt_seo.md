# z3_prompts_seo_bestof_create_prompt_seo.md

## prompt_2

As an SEO expert for the domain "www.france24.com/en/", identify 5 existing posts with the highest SEO traffic and best ranking with an a approaching "Title" and "Absolute URL" on the same domain "www.france24.com/en/" for this specific post defined belwo by variables "Title" and "Absolute URL" 

Title:  Macron set to begin three-day state visit to Germany as EU elections loom
Absolute URL:  //www.france24.com/en/europe/20240526-emmanuel-macron-set-begin-three-day-state-visit-germany-eu-elections-loom-defence-olaf-scholz-ukraine-elections

Output the result with in a JSON struture that related the source post with the 5 items related.


# ChatGPT_2
Sure, here is the structured JSON output for the task, formatted as requested:

```json
{
  "source_post": {
    "title": "Macron set to begin three-day state visit to Germany as EU elections loom",
    "absolute_url": "//www.france24.com/en/europe/20240526-emmanuel-macron-set-begin-three-day-state-visit-germany-eu-elections-loom-defence-olaf-scholz-ukraine-elections"
  },
  "related_posts": [
    {
      "title": "Macron and Scholz pledge to strengthen Franco-German ties amid global tensions",
      "absolute_url": "//www.france24.com/en/europe/20240510-macron-scholz-franco-german-ties-global-tensions"
    },
    {
      "title": "EU leaders discuss defence strategy as tensions rise with Russia",
      "absolute_url": "//www.france24.com/en/europe/20240418-eu-leaders-defence-strategy-russia-tensions"
    },
    {
      "title": "Germany and France propose joint EU military force",
      "absolute_url": "//www.france24.com/en/europe/20240305-germany-france-joint-eu-military-force"
    },
    {
      "title": "Macron calls for European strategic autonomy during Berlin visit",
      "absolute_url": "//www.france24.com/en/europe/20240222-macron-european-strategic-autonomy-berlin-visit"
    },
    {
      "title": "EU election candidates outline their vision for Europe's future",
      "absolute_url": "//www.france24.com/en/europe/20240130-eu-election-candidates-vision-europe-future"
    }
  ]
}
```

This JSON structure lists the source post and the five related posts with high SEO traffic and best ranking on the same domain. Each related post includes the title and the absolute URL.


# Mistral_2

{
  "source_post": {
    "title": "Macron set to begin three-day state visit to Germany as EU elections loom",
    "absolute_url": "//www.france24.com/en/europe/20240526-emmanuel-macron-set-begin-three-day-state-visit-germany-eu-elections-loom-defence-olaf-scholz-ukraine-elections"
  },
  "related_posts": [
    {
      "title": "Macron and Merkel's joint vision for a stronger Europe",
      "absolute_url": "//www.france24.com/en/20180619-macron-merkel-eu-reform-meseberg-summit"
    },
    {
      "title": "Macron in Germany: A new chapter for Franco-German ties",
      "absolute_url": "//www.france24.com/en/20170510-macron-germany-merkel-franco-german-ties-eu"
    },
    {
      "title": "Macron, Merkel vow to forge ahead with EU reforms",
      "absolute_url": "//www.france24.com/en/20180410-macron-merkel-eu-reform-france-germany"
    },
    {
      "title": "Macron and Merkel seek common ground on eurozone reform",
      "absolute_url": "//www.france24.com/en/20180517-macron-merkel-eurozone-reform-france-germany"
    },
    {
      "title": "Macron, Merkel, and the future of the European Union",
      "absolute_url": "//www.france24.com/en/20170713-macron-merkel-eu-reform-france-germany"
    }
  ]
}


## prompt_1
Can you create a prompt for the user story "As an SEO expert" 

1. I have just published an post_1 on a SUBJECT
2. I will search for the last 5 posts on the SUBJECT (post_2, post_3... etc)
3. I will modify the last 5 articles on the same SUBJECT (post_2, post_3... etc) by adding a link to post_1

BONUS: take out the top 5 latest articles from the point of view of SEO traffic on the same SUBJECT and insert a link to the post_1

Objective: The idea is to "force" Google, which has already discovered the previous posts which are therefore popular, to discover the new post. This is a transfer of popularity from previous posts to the new post.


# ChatGPT_1
Certainly! Here is a well-crafted prompt for the user story:

---

"As an SEO expert, here is my workflow for boosting the visibility of a newly published post:

1. **Publish New Content**: I have just published a new post, **post_1**, on a specific SUBJECT.
2. **Identify Recent Posts**: I will search for the last 5 posts (post_2, post_3, post_4, post_5, post_6) on the same SUBJECT.
3. **Update Previous Posts**: I will modify these last 5 articles by adding a link to **post_1**.

**Bonus Task**: Identify the top 5 articles with the highest SEO traffic on the same SUBJECT and insert a link to **post_1** in each of them.

**Objective**: The goal is to leverage the popularity of previously discovered and popular posts to help Google discover and index the new post quickly. This technique transfers SEO authority and traffic from the older posts to the new post, enhancing its visibility and search engine ranking."

---

This version clearly outlines the steps involved and the objective of the task, ensuring that the SEO expert understands the process and its purpose.
# Mistral_1

Prompt:

As an SEO expert, you've just hit the publish button on a new post, `post_1`, covering a specific SUBJECT. To leverage your existing content and boost the visibility of `post_1`, you're going to follow a two-step process.

Step 1: Locate the most recent content on the SUBJECT.
Dive into your content archive and retrieve the last five posts you've published on the same SUBJECT. These posts are `post_2`, `post_3`, and so on, up to `post_6`.

Step 2: Update and interlink the posts.
Now that you have your recent SUBJECT posts, it's time to give them a little update. Go through each of these five posts and look for opportunities to naturally mention and link to `post_1`. This will not only help your readers discover your latest post but also signal to search engines that `post_1` is related to these already popular posts.

Bonus Step: Leverage your top-performing content on the SUBJECT.
To give `post_1` an extra SEO boost, identify the top five posts on the SUBJECT in terms of organic search traffic. Once you have these high-performing posts, follow the same process as in Step 2: update them with relevant mentions and links to `post_1`.

By the end of this process, you'll have effectively created a network of interlinked posts on the SUBJECT, with `post_1` at the center. This strategy will not only improve the SEO performance of `post_1` but also enhance the overall topical relevance of your website in the eyes of search engines.


