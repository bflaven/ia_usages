

## PROMPT_6
I am fine with the evolutions in the plugin `breadcrumb-migration` Version v1.16.0 but I want a better UX.

1. Add a tab "Help Wikidata" after "Bulk Description" so I can if want have access to the inforamtion on how-to. Make the page look nice and ux frindly. Think insection as I may add some help section. Gotcha ? I gave the example of `augmented journalism` use it.


2. Go for an external JSON, for a few practical reasons cause I can update

- One source of truth, multiple consumers. Your plugin's PHP backend can read it with json_decode( file_get_contents( $path ), true ), but the same file is also directly usable by JavaScript in the WP admin, by your Python pipelines (MMA_semantic_light), or by Claude Code itself when it needs to inspect the data. The PHP array is only usable by PHP.
Safer. A .php data file is executable code — if it's ever writable or tampered with, it runs. JSON is inert data; worst case, parsing fails.

- Easier to extend. If tomorrow you want ten concepts instead of one (data journalism, OSINT, etc.), editing or programmatically generating JSON is trivial. Claude Code is also noticeably better at safely modifying JSON than at editing PHP arrays without breaking syntax.

- It's the lingua franca of Wikidata anyway. The Wikidata API speaks JSON, so if your plugin ever queries or pushes to Wikidata directly, you're already in the right format.




```txt
How to add "augmented journalism" to Wikidata

Step 1 - Create the item
Go to https://www.wikidata.org/wiki/Special:NewItem
Fill in the fields:
- Language: en
- Label: augmented journalism
- Description: journalistic practice combining human expertise with artificial intelligence to assist reporting, data analysis and fact-checking while keeping editorial judgment human
- Aliases (pipe-separated): AI-assisted journalism | augmented journalist
Click "Create". Wikidata assigns the item a unique QID.

Step 2 - Add statement: subclass of -> journalism
On the item page, in the Statements section, click "+ add statement".
- Property: type "subclass of" and select P279
- Value: type "journalism" and select Q11030
Click "publish".

Step 3 - Add statement: uses -> artificial intelligence
Click "+ add statement" again.
- Property: type "uses" and select P2283
- Value: type "artificial intelligence" and select Q11660
Click "publish".

Step 4 - Add a reference (recommended)
Under each statement, click "add reference".
- reference URL (P854): link to a source supporting the claim
- retrieved (P813): today's date
Click "publish". References protect new items from deletion for lack of notability.

Result
The item is now searchable on Wikidata, linked to the knowledge graph as a subclass of journalism (Q11030) that uses artificial intelligence (Q11660), and usable for entity linking via its QID.

If you want, I can also format this as a PHP array or JSON structure (steps, properties, QIDs) so it's directly consumable by your WordPress plugin rather than as prose.
```
```json
{
  "howto": {
    "id": "wikidata-augmented-journalism",
    "title": "How to add 'augmented journalism' to Wikidata",
    "item": {
      "language": "en",
      "label": "augmented journalism",
      "description": "journalistic practice combining human expertise with artificial intelligence to assist reporting, data analysis and fact-checking while keeping editorial judgment human",
      "aliases": ["AI-assisted journalism", "augmented journalist"]
    },
    "steps": [
      {
        "step": 1,
        "name": "Create the item",
        "url": "https://www.wikidata.org/wiki/Special:NewItem",
        "instructions": "Fill in Language (en), Label, Description and Aliases (pipe-separated), then click 'Create'. Wikidata assigns the item a unique QID.",
        "fields": {
          "language": "en",
          "label": "augmented journalism",
          "description": "journalistic practice combining human expertise with artificial intelligence to assist reporting, data analysis and fact-checking while keeping editorial judgment human",
          "aliases_input": "AI-assisted journalism | augmented journalist"
        }
      },
      {
        "step": 2,
        "name": "Add statement: subclass of -> journalism",
        "instructions": "In the Statements section, click '+ add statement'. Select the property, select the value, then click 'publish'.",
        "statement": {
          "property": { "id": "P279", "label": "subclass of" },
          "value": { "id": "Q11030", "label": "journalism" }
        }
      },
      {
        "step": 3,
        "name": "Add statement: uses -> artificial intelligence",
        "instructions": "Click '+ add statement' again. Select the property, select the value, then click 'publish'.",
        "statement": {
          "property": { "id": "P2283", "label": "uses" },
          "value": { "id": "Q11660", "label": "artificial intelligence" }
        }
      },
      {
        "step": 4,
        "name": "Add a reference (recommended)",
        "instructions": "Under each statement, click 'add reference'. Add a reference URL and the retrieval date, then click 'publish'. References protect new items from deletion for lack of notability.",
        "reference_properties": [
          { "id": "P854", "label": "reference URL", "value": "URL of a source supporting the claim" },
          { "id": "P813", "label": "retrieved", "value": "today's date" }
        ]
      }
    ],
    "result": "The item is searchable on Wikidata, linked to the knowledge graph as a subclass of journalism (Q11030) that uses artificial intelligence (Q11660), and usable for entity linking via its QID."
  }
}
```

## PROMPT_5
Summarize simply and precisely the way you add `augmented journalism` to wikidata like a how-to with Suggested statements:
subclass of -> `journalism` (Q11030)
uses -> `artificial intelligence` (Q11660)
This how-to will be added to a wordpress plugin that I am currently doing with claude code










## PROMPT_4
journalistic practice combining human expertise with artificial intelligence to assist reporting, data analysis and fact-checking while keeping editorial judgment human


augmented journalism

journalistic practice combining human expertise with artificial intelligence to assist reporting, data analysis and fact-checking while keeping editorial judgment human

Shorter alternative:

journalism enhanced by artificial intelligence tools under human editorial control

Possible aliases: 

Suggested statements: subclass of -> journalism (Q11030), uses -> artificial intelligence (Q11660)


When you talk about Possible aliases.
It means that when I will create the word on wikidata. I can add in field Aliases, pipe-separated. The following stuff: 
AI-assisted journalism | augmented journalist




## PROMPT_4
I am fine with the evolutions in the plugin `breadcrumb-migration` Version 1.15.0 bu I want a better UX.

1. In the tab "Bulk Assign", I want 2 sections or 2 steps e.g you can use `<section></section>` to mark out the steps or sections. Feel free to make propositions for each title section.
In first step or section, I should be able to cut and paste in bm-bulk-keywords a list of keywords and search if they have first a default parent category e.g Tunisian Arabic, user stories, vectorization, version control, Whisper, Wolof, Wordpress, Yoruba, Zulu. 
In second step or section, I should able to select
2. In the tab "Bulk Description", I need to know with color code the status for each row. Indicate also the below "Requirements" with a your choice name that explain the color code. Use light color because it has to remain readable. Let's say
light green: the status is published and everything has  been completed and the breadcrumb is published in the frontend. I don't have to give a shit about these tags. You can add a filter also "Completed" as a checkbox.
light orange: there is something wrong eg Wikidata ID empty or Wikidata description empty or Actual description empty
light red : this shit storm there is nothing, no Wikidata ID empty and no Wikidata description empty and no Actual description empty.

3. For every filter indicate the number of tags available at the right of the button "Show all". By default, when it is "Show all", show at the same place the total amount of tags. Be carful with these changes, I do not want to shatter the performance for a fucking UX enhancement so challenge me if it is not possible.

Note: Before coding, summarize in bullet points that you understand from the given instructions. Update the readme in the changelog in the readme and the version of the plugin when I validate the changes asked.


## PROMPT_3
Add this change below to the existing list.
One more change. I have made a manual edit of a selected tag and added Description so I should be able to see in the column Actual Description if I had a refresh button somewhere near "Edit in WP". It should not be "Empty". You need also to flag the porcess of creating a description because it means that is handwriting description made by me an that is fucking precious because even is there is Wikidata ID or no Wikidata ID the description wa unavailable so I had to write to it down, I do not want to loose it but i want to know that these description has been written by me and do not need to be synchronize.
Note: Before coding, summarize in bullet points that you understand from the given instructions. Update the readme in the changelog in the readme and the version of the plugin when I validate the changes asked.



## PROMPT_3
Add this change below to the existing list.
One more change. I have made a manual edit of a selected tag and added Description so I should be able to see in the column Actual Description if I had a refresh button somewhere near "Edit in WP". It should not be "Empty". You need also to flag the porcess of creating a description because it means that is handwriting description made by me an that is fucking precious because even is there is Wikidata ID or no Wikidata ID the description wa unavailable so I had to write to it down, I do not want to loose it but i want to know that these description has been written by me and do not need to be synchronize.
Note: Before coding, summarize in bullet points that you understand from the given instructions. Update the readme in the changelog in the readme and the version of the plugin when I validate the changes asked.

## PROMPT_2

I am fine with the evolutions in the plugin `breadcrumb-migration` Version 1.14.0 bu I want a better UX.

1. On the tab "Bulk Description", the screen is now a bit messy, you should each function in a tag `<section></section>`  or something that separates each function so we can easily identify the function in the Bulk Description main section. Capisce ?

2. For tout information, I just make a proposition of section names. Find a better and shorter name, the most functional and english native speaking eg american or english who cares :)
e.g 
section_1 -> Caution using Bulk Description
section_2 -> Search tag
section_3 -> Filter by tag names
section_4 -> Working by row.
Do do use section_#NB -> as name ! it is just for educational purposes, make some good suggestions yourself.
3. For the caution message, it is fucking messy. Be more direct and explicit, enumerate the conditions required to enable the edition of each tag because I will probably forget the requirements to have the opportunity to see tags in this page. Gotcha ? I just give you some orientation, it is just for educational purposes, make some good propositions yourself.

Use after Bulk Assign: 
	i. You must assign a default category to each tag so the tag is available in the tab "Bulk Description"
	ii. You must validate but not necessary publish.

Note: Before coding, summarize in bullet points that you understand from the given instructions. Update the readme in the changelog in the readme and the version of the plugin when I validate the changes asked.



## PROMPT_1

I am fine with the plugin but I want some evolutions in the plugin `breadcrumb-migration`, mostly UX.
1. On the tab "Bulk Description", I want to be able to edit and synchronize the "Actual Description" if I fill it by editing the tag e.g `wp-admin/term.php?taxonomy=post_tag&tag_ID=2427&post_type=post`. For instance I have edited this tag (tag_ID=2427) and added a tag Description so I want to see the value in "Actual Description" by any means, I can have a button to synchronize e.g. Synchronize.

2. On the tab "Bulk Description", in Description from Wikidata, if the Description from Wikidata is filled, I should be able for each tag to copy the description to Actual Description so I have a clear view of the editorial status of each tag and say row by row if it is OK or not.

3. I should have on the right of the "Actual Description" a link that leads to the edit tag and and at the right of the tag_ID in input type="text".


4. On the tab "Bulk Description", you can add a section where I cut and paste in a textarea a bunch of comma separated tags e.g `Apidoc, Chai, cheerio, CRUD, ejs, Express, Javascript, MySQL, Node, pug, Test, view-engines, Webapp, Node, Express, MySQL, CRUD`. For your information, I have already put a default category, so these tags are already in the listing of the tabs "Bulk Description". Iit will help to find and select a certain amount of tags, make the call to wiidata or edit the tag description and cut and paste it if you implement the asked  feature above... I am looking for anything that speeds up the process. Capisce?


5. Think of any evolution, feature, quickwins that will help to reduce time consuming actions for each tag. For instance I was thinking of searching like you have on `/wp-admin/edit-tags.php?taxonomy=post_tag`. Capisce?


Note: Before coding, summarize in bullet points that you understand from the given instructions. Update the readme in the changelog in the readme and the version of the plugin when I validate the changes asked.



## DEPOT
- wikidata extension for tag contribution
```txt
Alexandre Brachet is the founder of the production company UPIAN, a pioneer in web documentaries and transmedia production.
```
- categories
```txt
APIs & Integration, 
Business & Case Studies, 
Cloud & Infrastructure, 
Data & Analytics, 
Programming & Databases, 
Technology & Trends, 
Tools & Productivity, 
Tutorials & How-to, 
Web Development
```


- tags
```txt
Apidoc, Chai, cheerio, CRUD, ejs, Express, Javascript, MySQL, Node, pug, Test, view-engines, Webapp, Node, Express, MySQL, CRUD
```

