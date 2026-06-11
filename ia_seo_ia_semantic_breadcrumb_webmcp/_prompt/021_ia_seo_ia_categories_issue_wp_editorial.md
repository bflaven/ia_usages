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

