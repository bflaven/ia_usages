## PROMPT_1

I need a better UX for the plugin `Breadcrumb Migration Version Version 1.33.0`, through use, I discovered that the plugin needs improvements. Here are the changes needed that should take into account these observations.


1. The files are in `breadcrumb-migration`.
2. In the tab "Bulk Description", I need to add a search box like in the tags wp native page . See model code below, just for the look and feel `- 1. search box model code for tags`
3. In the tab "Bulk Description", I need to add a pagination with 2O items like in the tags wp native page . See model code below, just for the look and feel `- 2. pagination box model code for tags`
4. In the tab "Bulk Description", I need to add a pagination with 2O items like in the tags wp native page 
5. Add Wikidata ID filled as filter inside the filters.
6. Rearrange with the best UX as WP model to ease the usage of all these functions as they are many. Find the better UX to expose these features that have a direct impact on the manipulation of the dataset below. The code is just given as example, feel free to get inspiration but find the best UX.


NOTE: Before coding, summarize in bullet points that you understand from the given instructions. Update the readme in the changelog in the readme and the version of the script when I validate the changes asked.


- 1. search box model code for tags
```html
<p class="search-box">
  <label class="screen-reader-text" for="tag-search-input">Search Tags:</label>
  <input type="search" id="tag-search-input" name="s" value="" data-dashlane-rid="348e92e0c39a8e9e">
    <input type="submit" id="search-submit" class="button" value="Search Tags" data-dashlane-rid="9d42f0b95ff3a056"></p>
```
- 2. pagination box model code for tags
```html
<div class="tablenav-pages"><span class="displaying-num">2,605 items</span>
<span class="pagination-links"><span class="tablenav-pages-navspan button disabled" aria-hidden="true">«</span>
<span class="tablenav-pages-navspan button disabled" aria-hidden="true">‹</span>
<span class="paging-input"><label for="current-page-selector" class="screen-reader-text">Current Page</label><input class="current-page" id="current-page-selector" type="text" name="paged" value="1" size="3" aria-describedby="table-paging" data-dashlane-rid="cdce22e6b87df1d2" data-dashlane-classification="other"><span class="tablenav-paging-text"> of <span class="total-pages">131</span></span></span>
<a class="next-page button" href="http://localhost:8080/wp-admin/edit-tags.php?taxonomy=post_tag&amp;paged=2"><span class="screen-reader-text">Next page</span><span aria-hidden="true">›</span></a>
<a class="last-page button" href="http://localhost:8080/wp-admin/edit-tags.php?taxonomy=post_tag&amp;paged=131"><span class="screen-reader-text">Last page</span><span aria-hidden="true">»</span></a></span></div>
```
- 3. filters for tags
```html
<div class="bm-bulk-desc-filters" id="bm-bulk-desc-filters">
        <strong>Show only:</strong>
        <label>
          <input type="checkbox" id="bm-filter-wd-id-empty" class="bm-desc-filter">
          Wikidata ID empty         <span class="bm-filter-count" id="bm-count-wd-id-empty">25</span>
        </label>
        <label>
          <input type="checkbox" id="bm-filter-wd-desc-empty" class="bm-desc-filter">
          Wikidata description empty          <span class="bm-filter-count" id="bm-count-wd-desc-empty">34</span>
        </label>
        <label>
          <input type="checkbox" id="bm-filter-actual-desc-empty" class="bm-desc-filter">
          Actual description empty          <span class="bm-filter-count" id="bm-count-actual-desc-empty">34</span>
        </label>
        <label>
          <input type="checkbox" id="bm-filter-manual-only" class="bm-desc-filter">
          Written (manual) only         <span class="bm-filter-count" id="bm-count-manual-only">5</span>
        </label>
        <label>
          <input type="checkbox" id="bm-filter-completed" class="bm-desc-filter">
          Completed         <span class="bm-filter-count" id="bm-count-completed">560</span>
        </label>
        <button type="button" class="button button-small" id="bm-desc-filter-reset">
          Show all        </button>
        <p class="bm-desc-search-box">
          <label class="screen-reader-text" for="bm-desc-name-search">
            Search Tags:          </label>
          <input type="search" id="bm-desc-name-search" class="bm-desc-name-search" placeholder="Search tags…">
          <input type="submit" id="bm-desc-search-submit" class="button button-small" value="Search Tags">
        </p>
        <span class="bm-filter-visible-count">
          <span id="bm-desc-visible-count">594</span> / <span id="bm-desc-total-count">594</span>
        </span>
      </div>
```

