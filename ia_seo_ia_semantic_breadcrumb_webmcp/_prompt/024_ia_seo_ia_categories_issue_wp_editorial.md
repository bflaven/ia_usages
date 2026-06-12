## PROMPT_1


I am fine with the evolutions in the plugin `breadcrumb-migration` Version 1.18.0 but I want a better UX.

1. Can you extend the functionality in tab "Bulk Assign", I want for instance to look for the default category for the following keywords list : `API, Chai, Faker, Javascript, json-server, Newman, Postman, Tests`
- SET_1 `API, Chai, Javascript, Newman, Postman` has already a default category e.g `Web Development`
- SET_2 `Faker, json-server, Postman, Tests` has a default category  "— none —" for default category assigned 

So on the right of the column `Keyword`, I want a column where I can check row by row the keyword that I want to set a default category  e.g `Web Development`. Add also on the top of the column an "All" checkbox that will check all the rows. The objective is to set row by row the keywords for the SET_2 and then decide to assign a default category.  


2. Under the bm-bulk-check-results, I want a textarea that show a comma separated list of the selected keywords e.g SET_2 because I can then cut and paste for another usage.

3. Can you extend the functionality in tab "Bulk Description", when I use the "Batch Filter" section, the UX is not optimal for instance I use the list `API, Chai, Faker, Javascript, json-server, Newman, Postman, Tests` whenever I am clicking on any button in the result widefat striped bm-bulk-desc-table the table lose the focus when I am not working anymore on the set I have previously selected `API, Chai, Faker, Javascript, json-server, Newman, Postman, Tests`. Can you do something about it, ideally I want a persistence of the selection of the keyword list selected.

4. In the tab "Bulk Description", remove the function "Quick Find", I found it unclear. It means I type e.g niger It shows the result widefat striped bm-bulk-desc-table but the the button "↺ Synchronize from WordPress" does provide any utility. You should put instead this function something like in Wordpress in the tags page inside the bm-bulk-desc-filters on the right. The code is only given as an example.
```html
<p class="search-box">
	<label class="screen-reader-text" for="tag-search-input">Search Tags:</label>
	<input type="search" id="tag-search-input" name="s" value="" data-dashlane-rid="67e2581384cd8590">
		<input type="submit" id="search-submit" class="button" value="Search Tags" data-dashlane-rid="a8c36aa5459f98c4"></p>
```
Same UX deficient as point 3 in "Batch Filter" section, losing the focus if I use the search.

Note: Before coding, summarize in bullet points that you understand from the given instructions. Update the readme in the changelog in the readme and the version of the plugin when I validate the changes asked.




