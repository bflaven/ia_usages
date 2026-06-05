## === Breadcrumb Category Migration ===
Contributors: brunoflaven
Donate link: https://flaven.fr/
Tags: categories, migration, taxonomy, breadcrumbs, redirects, drag and drop, multi-select, multicategorization, htaccess
Requires at least: 5.0
Tested up to: 6.5
Stable tag: 1.2.0
Requires PHP: 7.4
License: GPLv2 or later
License URI: https://www.gnu.org/licenses/gpl-2.0.html

*** 

Two-tab admin tool for progressive taxonomy management. **Migration tab**: drag & drop (with multi-select) to add target categories to posts while keeping source categories intact — enabling multi-categorization. **Reduction tab**: point-and-click generator for `Redirect 301` .htaccess directives — pair a source category with a target, accumulate all lines, copy them in one shot. Optionally delete empty old categories.

## == Description ==

**Breadcrumb Category Migration** provides an interactive admin tool to help you clean up and migrate your category taxonomy gradually, instead of doing everything in one shot via CSV or SQL.

It adds a dedicated two-tab page under **Tools → Breadcrumb Migration** (`?page=breadcrumb-migration-category-migration`) where you can:

- See **source categories** (typically legacy or French categories) on the left.
- See **target categories** (your new English “pillar” categories) on the right.
- List all **posts in a selected source category** in the middle, with a **Select All / Deselect All** toolbar.
- **Click rows or checkboxes** to multi-select posts.
- **Drag one or multiple selected posts** to a target category to add that category — source categories are always kept.
- When a source category becomes empty, **delete it** and get a ready-made **.htaccess redirect** line to keep SEO value.
- On the **Reduction tab**: click a source category, click a target category → get a `Redirect 301` line instantly; accumulate all pairs into a textarea and copy them in one shot for your `.htaccess`.

This is especially useful when:

- You want to **multi-categorize** posts progressively (a post can belong to many pillar categories).
- You are migrating from a messy, multilingual taxonomy to a clean English‑only taxonomy.
- You want to pre-generate all `.htaccess` redirects without needing to empty categories first.

The plugin does *not* automatically manage redirects on the frontend; instead, it generates the `Redirect 301` / `Redirect 410` snippets for you to paste into `.htaccess`.

## == Features ==

- Admin page at `Tools → Breadcrumb Migration` (slug: `breadcrumb-migration-category-migration`).
- Left column: list of **source categories** (non‑pillar or legacy categories).
- Middle column: **posts in the selected source category**, each row selectable and draggable.
  - **Select All / Deselect All** toolbar button.
  - Click a row or its checkbox to toggle selection (highlighted in blue).
  - Drag any selected row — all selected posts are dragged together (custom ghost shows count).
  - Drag an unselected row — only that single post is dragged.
- Right column: list of **target (pillar) categories** as drop zones (live post count displayed).
- Drop one or multiple posts onto a target category:
  - **Adds** the target category to every dropped post.
  - **Source categories are never removed** — posts accumulate categories (multi-categorization).
  - Dropped post rows flash green as confirmation; target category count updates live.
  - A green feedback banner shows how many posts were added.
- After all posts are manually removed from a source category (count reaches 0):
  - A **”Delete & show redirect snippet”** button appears.
  - On click, the plugin deletes the category and prints a `.htaccess` line like:

    `Redirect 301 /category/old-slug/ /category/new-slug/`

- Redirect line is copy‑paste ready for both local and production environments (path‑only).
- **Reduction tab** — dedicated `.htaccess` redirect generator (no category deletion required):
  - Left column: source categories with slug visible.
  - Right column: target pillar categories with slug visible.
  - Click source + click target → preview shows `Redirect 301 /category/old/ /category/new/` immediately.
  - **Copy line** button: copies the single directive to clipboard.
  - **Add to list** button: appends the line to the accumulated textarea; source item is marked with strikethrough to track progress.
  - **Copy All** button: copies every accumulated directive at once — ready to paste into `.htaccess`.
  - **Clear list** button: resets the textarea and processed markers.
  - No AJAX writes; purely client-side after initial category load.

== Installation ==

1. Upload the plugin folder:

   - Copy the folder `breadcrumb-migration-category-migration` into `wp-content/plugins/`.
   - The main file should be: `wp-content/plugins/breadcrumb-migration-category-migration/breadcrumb-migration-category-migration.php`.

2. Activate the plugin:

   - Go to **Plugins → Installed Plugins**.
   - Activate **Breadcrumb Category Migration**.

3. Configure the **pillar category IDs**:

   - Edit `breadcrumb-migration-category-migration.php`.
   - In the method `ajax_get_target_categories()`, update the `$pillar_ids` array to contain the term IDs of your **pillar (target) categories**.
   - Optionally, also update `$pillar_ids` in `ajax_get_source_categories()` to *exclude* pillar categories from the source list.

Term IDs can be obtained from:

- **Posts → Categories** (hover over a category to see `tag_ID` in the URL).
- Or from a category CSV export.

== Usage ==

### 1. Open the migration page

1. In the WordPress admin, go to **Tools → Breadcrumb Migration**.
2. The URL will be:

   `https://your-site.com/wp-admin/tools.php?page=breadcrumb-migration-category-migration`

You will see three columns:

- **Left** – Source Categories  
- **Center** – Posts in the selected category  
- **Right** – Target Categories  

### 2. Choose a source category

1. In the **Source Categories** panel (left), click on a category name.
2. The plugin loads all posts assigned to that category and shows them in the **middle column**.

Each post appears as a row with:

- Checkbox (left)
- Title
- Post ID

Rows are **selectable** (click row or checkbox) and **draggable**.

A **Select All / Deselect All** button appears above the list, along with the total post count.

### 3. Select and drag posts to target categories

**Selecting posts:**

- Click any row (or its checkbox) to toggle selection — selected rows highlight in blue.
- Click **Select All** to select every post in the list; click **Deselect All** to clear.

**Dragging:**

- Drag a **selected** row → all currently selected posts are dragged together. A ghost label shows the count (e.g., "5 posts").
- Drag an **unselected** row → only that single post is dragged.

**Dropping:**

1. Drop onto a target category box on the right.
2. A confirmation dialog appears:

   - Single post: `Add "Title" to "Target Category"?`
   - Multiple posts: `Add 5 posts to "Target Category"?`

3. Click **OK**:

   - The plugin calls `wp_set_post_terms()` with `$append = true` for each post.
   - **Source categories are preserved** — the post now belongs to both old and new categories.
   - Dropped post rows flash green; the target category’s post count updates live.
   - A green banner confirms the operation (e.g., "5 post(s) added to ‘Web Development’").

You can repeat this process to assign the same post to multiple target categories over time, building a full multi-categorization progressively.

### 4. Delete empty old category and get .htaccess redirect

Once a source category has **no posts left**:

1. The category line shows count `(0)` in the Source Categories list.
2. A button appears under the posts panel:

   **“Delete "Category Name" and show redirect snippet”**

3. Click the button:

   - You are asked to **confirm** the deletion.
   - Then you are prompted for the **target category slug** (without `/category/`), e.g. `web-development` or `3wdoc-tutorials`.
   - The plugin deletes the old category using `wp_delete_term()`.
   - It builds a redirect line and prints it, for example:

     `Redirect 301 /category/old-slug/ /category/web-development/`

4. Copy this line and paste it into your **.htaccess** file, above the `# BEGIN WordPress` block.

If you leave the target slug empty, the plugin generates a `Redirect 410` line:

- `Redirect 410 /category/old-slug/`

Use this when you really want to deprecate a category URL without redirecting it elsewhere.

### 5. Progressive migration

You can use this tool **gradually**:

- Work on one legacy category at a time:
  - Move its posts to one or several pillar categories.
  - Delete it once empty and add the redirect.
- Over time, you converge from a messy FR/legacy taxonomy to a clean EN/pillar taxonomy, with redirects preserving SEO.

== Frequently Asked Questions ==

= Does the plugin change category slugs or names automatically? =

No. This plugin focuses on **adding categories to posts** (multi-categorization) and optionally **deleting empty old categories**. It does not rename categories or change slugs by itself. You can combine it with your separate CSV‑based migration if you want to rename categories in bulk.

= Does it set redirects automatically on the frontend? =

No. The plugin only **prints .htaccess redirect lines** for you to copy‑paste. Redirects are handled by your web server (Apache) once you add those lines to `.htaccess`.

= Can I use it on production? =

Yes, but you should:

- Test thoroughly on staging first.
- Ensure you have full backups.
- Be careful when deleting categories and adding redirects.

= How do I choose source vs target categories? =

- **Target categories** are your EN “pillar” categories; configure their term IDs in `$pillar_ids` inside the plugin.  
- **Source categories** are all other categories by default (except those in `$pillar_ids`). You can refine this logic in `ajax_get_source_categories()` if needed.

= Does it handle custom taxonomies or custom post types? =

No. This version is focused on default `post` type and the `category` taxonomy. You can extend the code to support other taxonomies if required.

== Screenshots ==

1. Source, posts, and target columns on the migration page.
2. Posts list for the selected source category.
3. Redirect snippet displayed after deleting an empty category.

== Changelog ==

= 1.2.0 — 2026-05-13 =
* **New Reduction tab** — dedicated `.htaccess` redirect generator. Click source category + target category to preview `Redirect 301 /category/old/ /category/new/`. Add lines to an accumulated textarea, copy them all at once. No category deletion required.
* **Tab UI** — admin page now has two named tabs: "Migration" and "Reduction". Migration tab behavior is unchanged from v1.1.0.
* **Copy line / Copy All** buttons in Reduction tab use `navigator.clipboard` with `execCommand` fallback.
* **Processed markers** — source category rows in Reduction tab get strikethrough styling once added to the list; cleared by "Clear list".
* **Lazy init** — Reduction tab AJAX calls fire only when the tab is first opened (no wasted requests on Migration-only sessions).
* Category slug now displayed under the name in both Reduction columns for fast visual verification.
* **Fix: blank page on load** — replaced `wp_add_inline_script('jquery-core', …)` with a dedicated footer script handle (`wp_register_script` + `wp_enqueue_script`, `$in_footer = true`). The old approach caused both tabs to render empty when jQuery loaded deferred/async because `DOMContentLoaded` fired before the listener was registered. Script now runs in the footer where the DOM is already built; `DOMContentLoaded` listener removed. AJAX URL and nonce passed via `wp_localize_script` instead of PHP string interpolation. JS string rewritten as PHP heredoc to eliminate quote-escaping ambiguity.

= 1.1.0 — 2026-05-13 =
* **Additive categorization** — drop no longer removes source category from post; `wp_remove_object_terms()` removed. Posts accumulate categories for full multi-categorization support.
* **Multi-select posts** — checkbox on each post row; click row or checkbox to toggle selection (blue highlight).
* **Select All / Deselect All** toolbar button above the post list with live post count label.
* **Batch drag** — dragging a selected row carries all selected posts; custom ghost label shows count (e.g. "5 posts").
* **Bulk AJAX endpoint** — new `bf_bcm_bulk_add_post_category` action replaces `bf_bcm_move_post_category`; accepts `post_ids[]` array.
* **Visual feedback** — dropped post rows and target category box flash green on success; dismissing green banner after 3.5 s.
* **Live target count** — target category post count updates in the UI after each drop.
* Updated admin page description and inline help text to reflect additive-only behavior.

= 0.1.0 =
* Initial release with:
  * Tools → Breadcrumb Migration page.
  * Source/target categories loading via AJAX.
  * Drag & drop post reassignment between categories.
  * Delete empty category and generate .htaccess redirect line.

== Upgrade Notice ==

= 1.2.0 =
New Reduction tab for generating .htaccess Redirect 301 directives without touching the database. No breaking changes to Migration tab.

= 1.1.0 =
Behavior change: drops now ADD a category instead of moving the post. Source categories are no longer removed. Update any custom integrations that relied on the old `bf_bcm_move_post_category` AJAX action.

= 0.1.0 =
First public version. Test on staging and configure pillar IDs before using in production.