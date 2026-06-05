=== Breadcrumb Migration - Primary Category ===
Contributors: Bruno Flaven and mostly perplexity
Donate link: https://flaven.fr/
Tags: categories, primary category, bulk edit, editorial, ux
Requires at least: 5.0
Tested up to: 6.5
Stable tag: 1.1.0
Requires PHP: 7.4
License: GPLv2 or later
License URI: https://www.gnu.org/licenses/gpl-2.0.html

Define a primary category per post and set or clear it in bulk from the posts list, without changing your existing categories.

== Description ==

**Breadcrumb Migration - Primary Category** lets you choose which category is considered "primary" for each post, and then use that information in your theme. It is designed for editorial workflows where you want full control over the category displayed on the homepage, in meta, or in breadcrumbs, without breaking your existing taxonomy.

Key points:

- Adds a **Primary Category** meta box on the post edit screen.
- Lets you **bulk set** or **bulk clear** the primary category for many posts at once.
- Does **not** remove or change your normal categories – it only marks one of them as primary.
- Provides a simple helper function for themes to display the chosen primary category.

The plugin stores the choice in post meta and works with any theme that you adapt to use the helper.

== Features ==

- Select one primary category per post (or none).
- Only allows choosing among the categories already assigned to the post.
- Bulk action "Set primary category…" in the posts list.
- Bulk action "Clear primary category" in the posts list.
- Category selector above the posts list for bulk operations.
- Helper function: `bf_get_primary_category( $post_id )`.
- Compatible with existing category archives and SEO setups.

== Installation ==

1. Upload the plugin folder to your site:

   - Copy the folder `bf-primary-category` into `wp-content/plugins/`.
   - The main file should be: `wp-content/plugins/bf-primary-category/bf-primary-category.php`.

2. Activate the plugin:

   - Go to **Plugins → Installed Plugins**.
   - Activate **Breadcrumb Migration - Primary Category**.

3. (Optional but recommended) Adapt your theme to display the primary category:

   - Use the helper function `bf_get_primary_category()` in your templates.
   - See the “Theme integration” section below.

== Usage ==

### 1. Set primary category on a single post

1. Go to **Posts → All Posts** and click **Edit** on any post.
2. In the right sidebar (or meta boxes area), find the meta box **“Primary Category”**.
3. You will see:
   - One radio button **“No primary category”**.
   - One radio button for each category currently assigned to this post.
4. Select the category you want as primary **or** choose “No primary category”.
5. Click **Update** (or **Publish**) to save.

Notes:

- The plugin only allows picking a category that is already assigned to the post.
- If you later remove that category from the post, the plugin automatically clears the primary category meta on save.

### 2. Bulk set primary category for multiple posts

This lets you choose the same primary category for many posts at once.

1. Go to **Posts → All Posts**.
2. Above the list of posts, in the filters area, locate the dropdown:
   - `— Select primary category for bulk —`
3. Select the category you want to set as primary (for example, **HTML5**).
4. In the posts table, tick the checkboxes for all posts you want to affect.
5. In the **Bulk actions** dropdown, choose **“Set primary category…”**.
6. Click **Apply**.
7. You should see an admin notice:
   - `Primary category set for X posts.`
8. Edit any of the affected posts:
   - The **Primary Category** meta box should now show your chosen category selected.

Important:

- The plugin only sets the primary category for posts that already have the chosen category attached.
- Posts that do not have that category remain unchanged (no primary category set).
- This behavior is intentional to avoid silently changing your taxonomy; you can change it in code if you want to force-assign the category.

### 3. Bulk clear primary category for multiple posts

1. Go to **Posts → All Posts**.
2. Tick the checkboxes for the posts you want to update.
3. In the **Bulk actions** dropdown, choose **“Clear primary category”**.
4. Click **Apply**.
5. You should see an admin notice:
   - `Primary category cleared for X posts.`
6. Edit any affected post:
   - The **Primary Category** meta box will show **“No primary category”** selected.

### 4. Theme integration (display the primary category)

The plugin exposes a helper function:

```php
bf_get_primary_category( $post_id = null );
```

- Returns a `WP_Term` object for the primary category, or `null` if none is set.
- `$post_id` is optional; if not provided, the current post in the loop is used.

Example usage in a theme template:

```php
$primary_cat = bf_get_primary_category();

if ( $primary_cat instanceof WP_Term ) {
    echo '<a href="' . esc_url( get_category_link( $primary_cat->term_id ) ) . '">';
    echo esc_html( $primary_cat->name );
    echo '</a>';
}
```

#### Example: integrating with the Zaatar theme (allium_post_first_category)

If your theme uses a function similar to:

```php
function allium_post_first_category( $before = '', $after = '' ) {
    $categories = get_the_category();
    if ( $categories ) {
        // ...
    }
}
```

You can replace it with:

```php
if ( ! function_exists( 'allium_post_first_category' ) ) :
function allium_post_first_category( $before = '', $after = '' ) {

    $post_id = get_the_ID();
    if ( ! $post_id ) {
        return;
    }

    $cat = null;

    // 1. Try primary category from Breadcrumb Migration - Primary Category plugin.
    if ( function_exists( 'bf_get_primary_category' ) ) {
        $primary_cat = bf_get_primary_category( $post_id );
        if ( $primary_cat instanceof WP_Term ) {
            $cat = $primary_cat;
        }
    }

    // 2. Fallback to first category returned by get_the_category().
    if ( ! $cat ) {
        $categories = get_the_category( $post_id );
        if ( empty( $categories ) || ! isset( $categories ) ) {
            return;
        }
        $cat = $categories;
    }

    $html = sprintf(
        '<span class="post-first-category cat-links entry-meta-icon"><a href="%1$s" title="%2$s">%3$s</a></span>',
        esc_attr( esc_url( get_category_link( $cat->term_id ) ) ),
        esc_attr( $cat->name ),
        esc_html( $cat->name )
    );

    $html = $before . $html . $after;

    $html = apply_filters( 'allium_post_first_category_html', $html, array( $cat ) );

    echo $html;
}
endif;
```

This makes the theme use the primary category when available, and fall back to the previous behavior otherwise.

== Frequently Asked Questions ==

= Does this plugin change my categories or remove any assignments? =

No. The plugin does not remove or modify your existing category assignments. It only stores a **primary category ID in post meta** and reads it when needed.

= What happens if I remove the primary category from a post? =

If you remove the category from the post and then save, the plugin checks whether the stored primary category is still assigned. If not, it clears the primary category meta for that post.

= Can I force the bulk action to also assign the category to posts that do not have it? =

By default, the bulk action **only sets the primary category for posts that already have that category**. If you prefer to also assign that category to the posts, you can modify the bulk handler to call `wp_set_post_categories()` when needed.

= Does it work with custom post types or custom taxonomies? =

This initial version is focused on the default `post` post type and the `category` taxonomy. You can adapt the code to support other post types or taxonomies if needed.

== Screenshots ==

1. Primary Category meta box on the post edit screen.
2. Bulk primary category selector above the posts list.
3. Bulk actions dropdown with “Set primary category…” and “Clear primary category”.

== Changelog ==

= 1.1.0 =
* Fixed bulk handling by capturing the selected category before the bulk action runs.
* Improved admin notice and inline documentation.

= 1.0.0 =
* Initial release with per‑post meta box and basic bulk actions.

== Upgrade Notice ==

= 1.1.0 =
Fixes bulk primary category setting. Update if you use bulk actions to set the primary category.



