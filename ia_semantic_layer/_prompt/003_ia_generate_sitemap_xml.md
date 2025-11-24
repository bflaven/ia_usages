## PROMPT_1

As a python expert and sitemap validator expert, I want a python script that calls the api https://flaven.fr/wp-json/wp/v2/posts and generates a list of content for a sitemap file. The site is a wordpress site with all kinds of content types : page, posts, tags, categories, archives, custom post type, custom taxonomies... etc. Is it necessary foe a sitemap ?

1. It should include all the content from the Wordpress site.
2. The script should progress with the help of the pagination for each type of content type, from the most recent to the oldest. Fi x as variable the number the pagination for each content type and the number of items so i can update according what I found as number in the wp e.g total number of Posts 657, total number of Pages 15... etc so i can fix the limit for loop per content type. 
3. Here is below some url type to query to the API to grab everything.


- TYPES
```text
# home
https://flaven.fr/
# archive
https://flaven.fr/2023/10/
# tag
https://flaven.fr/tag/computer/
# post
https://flaven.fr/2025/10/rescuing-failed-ai-implementations-practical-explorations-with-n8n-ollama-geo/

# post categories
https://flaven.fr/category/applications-et-web-applications/
# post tags
https://flaven.fr/tag/ai-assistants/


# custom post type video
https://flaven.fr/videos/sustainable-ai-tracking-carbon-footprints-of-mistral-models-with-ollama-codecarbon/
# custom taxonomie for post type video
https://flaven.fr/videos-tags/anaconda/


# custom post type quote
https://flaven.fr/quotes/eduquer-cest-accepter-de-disparaitre-pour-que-lautre-vive-leducateur-prepare-toujours-sa-propre-mort-cest-parce-quil-le-sait-sans-vouloir-se-lavouer-quil-est-souvent-feroce-le-savoir/
# custom taxonomie for post type quote
https://flaven.fr/authors-quotes/jacques-natanson/
# custom taxonomie for post type quote
https://flaven.fr/flavors-quotes/idees/

# custom post type client
https://flaven.fr/clients/
# custom post type client item
https://flaven.fr/clients/radio-france-internationale-rfi/

```

- SITEMAP
```xml
<url><loc>https://flaven.fr/</loc><lastmod>2023-05-13T06:02:10+00:00</lastmod><priority>0.90</priority></url>

<url><loc>https://flaven.fr/</loc><lastmod>2023-05-13T06:02:10+00:00</lastmod><priority>0.90</priority></url>

<url><loc>https://flaven.fr/bruno-flaven-resume-cv/</loc><lastmod>2023-05-13T06:02:10+00:00</lastmod><priority>0.60</priority></url>

<url><loc>https://flaven.fr/publications/</loc><lastmod>2023-05-13T06:02:10+00:00</lastmod><priority>0.60</priority></url>

<url><loc>https://flaven.fr/videos/</loc><lastmod>2023-05-13T06:02:10+00:00</lastmod><priority>0.60</priority></url>

<url><loc>https://flaven.fr/about-3wdoc/</loc><lastmod>2023-05-13T06:02:10+00:00</lastmod><priority>0.60</priority></url>

<url><loc>https://flaven.fr/2023/05/as-po-for-a-personal-challenge-writing-a-e2e-suite-for-websites-and-for-mobile-apps-with-cypress-and-chat-gpt-turned-me-as-a-prompt-engineer/</loc><lastmod>2023-05-13T06:02:10+00:00</lastmod><priority>0.60</priority></url>

```


