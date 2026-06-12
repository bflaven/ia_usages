## PROMPT_3
I am fine with the evolutions in the plugin `breadcrumb-migration` Version 1.20.0 but I want a better UX.


1. In tab "Proposals", remove your version of this navigation

- VERSION_1
```html
<div class="bm-pagination"><span class="bm-pagination__info">Page 1 of 127 (2521 terms)</span><a href="https://flaven.fr/wp-admin/admin.php?page=breadcrumb-migration&amp;bm_taxonomy=all&amp;bm_state=all&amp;bm_search&amp;bm_wikidata_id&amp;bm_spacy&amp;paged=2" class="button">Next →</a></div>
```
2. Add a row, align on the right, in bm-term-list, at the top and at the bottom a more wp look-like navigation because I need to know the number of items and to move easily forward and backward. Do not lose the focus of the filter for instance if i select e.g person, i will browse the result among the set of tags with PERSON assigned. Do not lose focus.

- VERSION_2 the code is only given as an example.
```html
<div class="tablenav-pages"><span class="displaying-num">2,498 items</span>
<span class="pagination-links"><span class="tablenav-pages-navspan button disabled" aria-hidden="true">«</span>
<span class="tablenav-pages-navspan button disabled" aria-hidden="true">‹</span>
<span class="paging-input"><label for="current-page-selector" class="screen-reader-text">Current Page</label><input class="current-page" id="current-page-selector" type="text" name="paged" value="1" size="3" aria-describedby="table-paging" data-dashlane-rid="e646cba60c362c3f" data-dashlane-classification="other"><span class="tablenav-paging-text"> of <span class="total-pages">125</span></span></span>
<a class="next-page button" href="http://localhost:8080/wp-admin/edit-tags.php?taxonomy=post_tag&amp;paged=2"><span class="screen-reader-text">Next page</span><span aria-hidden="true">›</span></a>
<a class="last-page button" href="http://localhost:8080/wp-admin/edit-tags.php?taxonomy=post_tag&amp;paged=125"><span class="screen-reader-text">Last page</span><span aria-hidden="true">»</span></a></span></div>
```



## PROMPT_1

I am fine with the evolutions in the plugin `breadcrumb-migration` Version 1.18.0 but I want a better UX.


1. In tab "Bulk Assign", the step "2 Assign Parent Category to Keywords" has not been change. See the error. The SET_1 has already a default category `APIs &amp; Integration` so I have checked on the "1
Search Keywords — Check Existing Assignments" only the tags that has NO default category e.g "— none —" but in "2 Assign Parent Category to Keywords" you did not take into account the choice and you have assigned the same default category to all the tags! Capisce

- SET_1 `API, Chai, Javascript, Newman, Postman` has already a default category e.g `APIs &amp; Integration`
- SET_2 `Faker, json-server, Postman, Tests` has a default category  "— none —" for default category assigned -> all these tags should have by default `Web Development` as category and only these tags. That was the objective of the change asked.


Note: Before coding, summarize in bullet points that you understand from the given instructions. Update the readme in the changelog in the readme and the version of the plugin when I validate the changes asked.





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




