
## PROMPT_6
I am about to do the chnages on the staging aka the wp in docker so the best thing to do is to create a plugin :

1. It will make a backup with the same structure so I can rollback to the situaion adn redo the orpation if necessary and change the categories and the slug based on the correct files that are: bck_migration_categories_v4_[timestamp].csv, bck_redirects_categories_v4_[timestamp].csv

1. It will load and change the categories and the slug based on the correct files that are: migration_categories_v4.csv, redirects_categories_v4.csv

Summarize your comprehension before coding and make a full bullet proposition with a step by step.


## PROMPT_5


1. Need to refine the table completely, reaffect all items in old_name to the new_category
2. Add also the slug wp-compliant both for new and old
3; Question: all these changes require to have a redirection table e.g old_name_slug leads to new_category_slug. Is it a 403 ? Remind how to handle the redirections and what to do with the sitemap for instance, the .htaccess, everything to take advantage from the migration without losing natural referencing (SEO) 

- csv example extended
```text
old_name;new_category;old_name_slug;new_category_slug;status
"Accessibilité";"UX & Product Design";"/category/accessibilite/";"/category/ux-and-product-design";

...
```
Summarize your comprehension before coding and make a full bullet proposition with a step by step.

## A_PROMPT_5

Here’s how I understand your request and a concrete plan.

***

## 1. My understanding

- You now want to **formalize the taxonomy migration** into a CSV that:  
  - Maps every **old category name + slug** to a **new canonical category + slug**.  
  - Uses a structure like:  
    `old_name;new_category;old_name_slug;new_category_slug;status`.  
- You want to:  
  1) **Refine and complete** the mapping table (cover all current categories).  
  2) Add **WordPress‑compliant slugs** for both old and new categories in the CSV.  
  3) Use this CSV as the **source of truth for redirections** so that each old URL redirects to the correct new URL.  
- You’re asking:  
  - What kind of redirect is needed (it is **301**, not 403). [reddit](https://www.reddit.com/r/Wordpress/comments/dznkgk/if_i_change_category_slug_url_will_the_old_url/)
  - How to handle **.htaccess, sitemap, and SEO** so you keep as much ranking as possible during the migration. [urchindesign.co](https://urchindesign.co.za/seo-changing-woocommerce-categories/)

Below is a step‑by‑step proposal.

***

## 2. CSV design for migration + redirects

Goal: a **single CSV** that drives both category migration and redirects.

Use semicolon (`;`) as separator, for example:

```text
old_name;new_category;old_name_slug;new_category_slug;status;redirect_type
"Accessibilité";"UX & Product Design";"/category/accessibilite/";"/category/ux-and-product-design/";"migrate";"301"
"Big data";"Data & Analytics";"/category/big-data/";"/category/data-and-analytics/";"migrate";"301"
"Bigdata";"Data & Analytics";"/category/bigdata/";"/category/data-and-analytics/";"merge";"301"
"Telecommuting";"Business & Case Studies";"/category/telecommuting/";"/category/remote-work/";"migrate";"301"
"Non classé";"Miscellaneous / Other";"/category/non-classe/";"/category/miscellaneous/";"migrate";"301"
"Old temp cat";"";"/category/old-temp-cat/";"";"drop";"410"
```

Fields semantics:

- `old_name`: current category **label** in WP.  
- `new_category`: final category label in your new taxonomy (can be identical or different).  
- `old_name_slug`: old category URL path (relative, including `/category/.../`).  
- `new_category_slug`: new category URL path (relative). Empty if dropped.  
- `status`:  
  - `"migrate"` = rename/move to new category.  
  - `"merge"` = merge into an existing category.  
  - `"drop"` = category removed; may return 410 or redirect to a broader category / homepage.  
- `redirect_type`:  
  - `"301"` for permanent redirect (SEO‑friendly). [sunnyhq](https://sunnyhq.io/blog/how-to-manage-wordpress-slugs/)
  - `"410"` if you explicitly want “gone” (rare, only for junk you don’t want indexed anymore).  

You can derive `old_name_slug` from your existing export and `new_category_slug` based on your new naming rules.

***

## 3. Step‑by‑step plan

### Step 1 – Complete the mapping table

- Start from your category CSV and create the extended CSV with columns above.  
- For each old category:  
  - Decide its `new_category` (from your 15–25 English pillars).  
  - Generate `new_category_slug` as a **WP‑compliant slug** (lowercase, hyphens, ascii only). [sunnyhq](https://sunnyhq.io/blog/how-to-manage-wordpress-slugs/)
  - Set `status` properly: `migrate`, `merge`, or `drop`.  
  - For normal migrations/merges, set `redirect_type = "301"`.  

At the end you have **one line per old category**, no ambiguity.

### Step 2 – Apply category changes in WordPress

Use the mapping to actually modify the taxonomy:

- For `migrate` rows where `new_category` is **same concept, new label/slug**:  
  - Use `wp_update_term()` (WP‑CLI or PHP script) to update the existing term’s `name` and `slug`. [sunnyhq](https://sunnyhq.io/blog/how-to-manage-wordpress-slugs/)
- For `merge` rows where multiple old categories go into one new one:  
  - Ensure the target category exists (create if needed).  
  - For each old category:  
    - Reassign its posts to the **target category** using `wp_set_object_terms()` or WP‑CLI (`wp term list`, `wp term update`, `wp term merge` if plugin).  
    - Optionally delete the old empty categories (`wp_delete_term()`).  
- For `drop` rows:  
  - Optionally remove the category from posts (or keep as historical, but then you won’t redirect them).  
  - Typically: delete the old category once you’re sure.

You can drive this process with Python‑generated commands or a custom WP plugin that ingests the CSV.

### Step 3 – Build a redirect table from the CSV

From the same CSV, generate a **pure URL mapping**:

```text
source;target;redirect_type
"/category/accessibilite/";"/category/ux-and-product-design/";"301"
"/category/big-data/";"/category/data-and-analytics/";"301"
"/category/bigdata/";"/category/data-and-analytics/";"301"
"/category/old-temp-cat/";"";"410"
...
```

Logic:

- If `status` is `migrate` or `merge` and `new_category_slug` not empty → map old to new with 301. [urchindesign.co](https://urchindesign.co.za/seo-changing-woocommerce-categories/)
- If `status` is `drop` and you really want to kill it → either 410 or map to a broader category (e.g. `/category/technology/`).  

This table can feed:

- A redirect plugin (Redirection, Rank Math, Yoast Premium, AIOSEO, etc.). [aioseo](https://aioseo.com/docs/automatic-redirects-when-changing-the-post-slug/)
- Or .htaccess rules if you prefer server‑level redirects. [stackoverflow](https://stackoverflow.com/questions/19075004/redirecting-one-category-to-another-using-htacess-wordpress)

### Step 4 – Implement redirects (plugins or .htaccess)

**Option A – SEO/redirect plugin (easiest)**

- Install a redirect manager (e.g. Redirection, Rank Math, Yoast Premium, AIOSEO redirections). [bestwebsoft](https://bestwebsoft.com/blog/301-redirect-in-wordpress/)
- Import your CSV or configure rules in bulk (many plugins accept CSV import or batch creation).  
- For each row:
  - Source: `/category/.../`  
  - Target: `/category/.../`  
  - Type: **301 (Permanent)**  

**Option B – .htaccess (lighter, more manual)**

In `.htaccess` (before WordPress default rules), you can add:

```apache
Redirect 301 /category/accessibilite/ /category/ux-and-product-design/
Redirect 301 /category/big-data/ /category/data-and-analytics/
Redirect 301 /category/bigdata/ /category/data-and-analytics/
# For a "gone" resource:
Redirect 410 /category/old-temp-cat/
```

Or use `RedirectMatch` with patterns if multiple categories share patterns. [stackoverflow](https://stackoverflow.com/questions/19075004/redirecting-one-category-to-another-using-htacess-wordpress)

Key: use **301** for SEO‑preserving migrations, not 302, not 403, not 404. [bestwebsoft](https://bestwebsoft.com/blog/301-redirect-in-wordpress/)

### Step 5 – Update sitemap and internal links

**Sitemap**:

- If you use an SEO plugin (Yoast, Rank Math, AIOSEO), it will regenerate XML sitemaps with the new category URLs automatically after the changes. [slickplan](https://slickplan.com/blog/update-sitemap)
- If you rely on the native WP sitemap (`wp-sitemap.xml`), it also updates as you change categories. [wp-kama](https://wp-kama.com/handbook/sitemap/change-url)
- After migration:
  - Check the sitemap: old category URLs should **not** appear; only the new ones.  
  - In Google Search Console and Bing Webmaster Tools, keep the same sitemap URL; they’ll re‑crawl automatically. [slickplan](https://slickplan.com/blog/update-sitemap)

**Internal links**:

- Use a crawler (Screaming Frog, etc.) or a search‑replace tool to find hard‑coded `/category/old-slug/` links in posts, menus, widgets. [sunnyhq](https://sunnyhq.io/blog/how-to-manage-wordpress-slugs/)
- Replace them with the new URLs where possible. The redirects will catch the rest, but internal links should eventually point directly to the new URLs.

### Step 6 – Monitor SEO after migration

- In Google Search Console:  
  - Monitor coverage → check that new category URLs are indexed, and errors remain low. [slickplan](https://slickplan.com/blog/update-sitemap)
  - Check “Links” → ensure internal links now point to new URLs.  
- Rankings typically wobble a bit then stabilise if redirects are clean. [urchindesign.co](https://urchindesign.co.za/seo-changing-woocommerce-categories/)

***

## 4. Direct answers to your questions

- **Is it a 403?**  
  No. For changed slugs/categories you want to preserve, you must use **301 (permanent) redirects**. [bestwebsoft](https://bestwebsoft.com/blog/301-redirect-in-wordpress/)
  - 403 = forbidden, not appropriate here.  
  - 404 = not found; you want to avoid long‑term.  
  - 410 = gone; only for content you intentionally remove.

- **How to “take advantage” of the migration for SEO?**  
  - Clean taxonomy → clearer topical clusters and better internal linking.  
  - 301 redirects from all old category URLs to new ones.  
  - Updated sitemap and internal links so Google sees consistent structure. [urchindesign.co](https://urchindesign.co.za/seo-changing-woocommerce-categories/)

***

If you want next, we can:

- Draft a **template migration CSV** for your actual categories (using your sample export).  
- Or write a **small Python script** that:  
  - reads your current categories CSV + a mapping config,  
  - generates the `migration.csv` and `redirects.csv` ready to import into WP / a redirect plugin.


  






