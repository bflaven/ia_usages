## PROMPT_1

As a Docker and a WordPress expert, can you write a plugin with best practices that enable to load into Wordpress the values from `related_posts_embeddings_settings.sqlite`.

1. I want on each post edit, the ability to pick up the IDs in the table `post_related`. For instance, let's I edit the post `post_id` = 13091 (the main/anchor post). 

- For each row:
  - `related_post_id` = 12927, 12840, 12947, 12815, 11616.  
  - `similarity` = the cosine similarity between the embedding of 13091 and the embedding of the related post (0.55, 0.52, etc.).  
  - `rank` = 1–5, descending by similarity (1 is most similar, 5 is the fifth most similar).  

This matches what the script writes to `post_related`:
This is exactly the structure you need to later for my WP plugin
- Export `post_related` to MariaDB.  
- For a given `post_id` in your WP plugin, fetch `ORDER BY rank` (or `similarity DESC`) and display the 10 related posts by `related_post_id`. [apxml](https://apxml.com/courses/building-ml-recommendation-system/chapter-2-content-based-filtering/producing-content-based-recommendations)


## OUTPUT_1


You can do this cleanly with a small plugin that:

- Connects (read‑only) to `related_posts_embeddings_settings.sqlite`.  
- On post edit, queries `post_related` for the current post ID.  
- Displays the related posts (ID, title, similarity, rank) in a meta box.  

Below is a minimal but structured plugin you can drop into `wp-content/plugins/wp-related-embeddings/`.

***

## 1. Plugin structure and file name

Create:

`wp-content/plugins/wp-related-embeddings/wp-related-embeddings.php`

Paste the code below into that file.

This plugin assumes:

- Your SQLite file is at `wp-content/related_posts_embeddings_settings.sqlite`.  
- Table: `post_related (post_id, related_post_id, similarity, rank)`.  
- You want to show up to 10 related posts in the edit screen (you can change that constant).

If your SQLite file is elsewhere, you can adjust the path in the config section.

***

## 2. Plugin code (copy–paste)

```php
<?php
/**
 * Plugin Name: WP Related Posts via Embeddings
 * Description: Displays related posts in the post edit screen using data from related_posts_embeddings_settings.sqlite.
 * Version: 0.1.0
 * Author: Your Name
 * Text Domain: wp-related-embeddings
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * CONFIGURATION
 *
 * Adjust these constants to your environment.
 */

// Absolute path to the SQLite DB that contains post_related.
define(
    'WP_RELATED_EMBEDDINGS_SQLITE_PATH',
    WP_CONTENT_DIR . '/related_posts_embeddings_settings.sqlite'
);

// Maximum number of rows to display in the meta box for each post.
define( 'WP_RELATED_EMBEDDINGS_MAX_ROWS', 10 );


/**
 * Utility: get a PDO connection to the SQLite DB.
 *
 * Note: this is read-only logic; we do not write to SQLite from WP.
 */
function wp_re_emb_get_sqlite_pdo() {
    static $pdo = null;

    if ( $pdo instanceof PDO ) {
        return $pdo;
    }

    $db_path = WP_RELATED_EMBEDDINGS_SQLITE_PATH;

    if ( ! file_exists( $db_path ) ) {
        // Fail silently in UI; log for debugging.
        error_log(
            sprintf(
                '[wp-related-embeddings] SQLite file not found at %s',
                $db_path
            )
        );
        return null;
    }

    try {
        $dsn = 'sqlite:' . $db_path;
        $pdo = new PDO( $dsn );
        $pdo->setAttribute( PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION );
        return $pdo;
    } catch ( Exception $e ) {
        error_log(
            sprintf(
                '[wp-related-embeddings] Could not connect to SQLite DB: %s',
                $e->getMessage()
            )
        );
        return null;
    }
}


/**
 * Fetch related posts for a given post_id from SQLite.
 *
 * Returns an array of rows:
 *  [
 *    [
 *      'related_post_id' => 12927,
 *      'similarity'      => 0.5533,
 *      'rank'            => 1,
 *    ],
 *    ...
 *  ]
 */
function wp_re_emb_get_related_from_sqlite( $post_id ) {
    $pdo = wp_re_emb_get_sqlite_pdo();
    if ( ! $pdo ) {
        return array();
    }

    $sql = '
        SELECT related_post_id, similarity, rank
        FROM post_related
        WHERE post_id = :post_id
        ORDER BY rank ASC
        LIMIT :limit
    ';

    try {
        $stmt = $pdo->prepare( $sql );
        $stmt->bindValue( ':post_id', (int) $post_id, PDO::PARAM_INT );
        $stmt->bindValue( ':limit', (int) WP_RELATED_EMBEDDINGS_MAX_ROWS, PDO::PARAM_INT );
        $stmt->execute();

        $rows = array();
        while ( $row = $stmt->fetch( PDO::FETCH_ASSOC ) ) {
            $rows[] = array(
                'related_post_id' => (int) $row['related_post_id'],
                'similarity'      => (float) $row['similarity'],
                'rank'            => (int) $row['rank'],
            );
        }

        return $rows;
    } catch ( Exception $e ) {
        error_log(
            sprintf(
                '[wp-related-embeddings] Query error: %s',
                $e->getMessage()
            )
        );
        return array();
    }
}


/**
 * Meta box callback: render related posts from SQLite on the post edit screen.
 *
 * Shows:
 * - related_post_id
 * - title (if exists in WP)
 * - similarity
 * - rank
 */
function wp_re_emb_render_meta_box( WP_Post $post ) {
    $post_id      = $post->ID;
    $related_rows = wp_re_emb_get_related_from_sqlite( $post_id );

    echo '<p>';
    echo esc_html__( 'These related posts are computed offline from embeddings and read from SQLite.', 'wp-related-embeddings' );
    echo '</p>';

    if ( empty( $related_rows ) ) {
        echo '<p><em>' . esc_html__( 'No related posts found in SQLite for this post.', 'wp-related-embeddings' ) . '</em></p>';
        return;
    }

    echo '<table class="widefat fixed striped">';
    echo '<thead><tr>';
    echo '<th>' . esc_html__( 'Rank', 'wp-related-embeddings' ) . '</th>';
    echo '<th>' . esc_html__( 'Related Post', 'wp-related-embeddings' ) . '</th>';
    echo '<th>' . esc_html__( 'Similarity', 'wp-related-embeddings' ) . '</th>';
    echo '</tr></thead>';
    echo '<tbody>';

    foreach ( $related_rows as $row ) {
        $rel_id   = $row['related_post_id'];
        $rank     = $row['rank'];
        $sim      = $row['similarity'];
        $rel_post = get_post( $rel_id );

        echo '<tr>';

        // Rank
        echo '<td>' . esc_html( $rank ) . '</td>';

        // Related post title + link, if exists in WP
        echo '<td>';
        if ( $rel_post instanceof WP_Post ) {
            $title = get_the_title( $rel_post );
            $url   = get_edit_post_link( $rel_post );
            echo '<a href="' . esc_url( $url ) . '">';
            echo esc_html( sprintf( '%d – %s', $rel_id, $title ) );
            echo '</a>';
        } else {
            // The related_post_id is not (or no longer) a post in this WP.
            echo esc_html( sprintf( 'Post ID %d (not found in WP)', $rel_id ) );
        }
        echo '</td>';

        // Similarity (formatted)
        echo '<td>' . esc_html( number_format( $sim, 3 ) ) . '</td>';

        echo '</tr>';
    }

    echo '</tbody>';
    echo '</table>';
}


/**
 * Register the meta box on post edit screens.
 */
function wp_re_emb_add_meta_box() {
    add_meta_box(
        'wp_related_embeddings_meta_box',
        __( 'Related Posts (Embeddings)', 'wp-related-embeddings' ),
        'wp_re_emb_render_meta_box',
        'post',          // post type: standard posts
        'side',          // context: side column
        'default'        // priority
    );
}
add_action( 'add_meta_boxes', 'wp_re_emb_add_meta_box' );
```

This plugin:

- Does not write anything to WP DB; it only reads `post_related` from SQLite.  
- For the post you are editing (e.g. `post_id = 13091`), it queries rows like:

  - `related_post_id` = 12927, 12840, 12947, 12815, 11616  
  - `similarity` = 0.55, 0.52, …  
  - `rank` = 1–10 (depending on your pipeline settings)

- Shows them in a meta box with:
  - Rank.  
  - Related post ID + title (linking to edit screen if it exists in WP).  
  - Similarity score.

***

## 3. Making it match your DB name/path

Your Python script currently uses a file named something like `related_posts_embeddings_settings.sqlite` (you mentioned that name). In the plugin I used:

```php
define(
    'WP_RELATED_EMBEDDINGS_SQLITE_PATH',
    WP_CONTENT_DIR . '/related_posts_embeddings_settings.sqlite'
);
```

So:

- Put your SQLite file at: `wp-content/related_posts_embeddings_settings.sqlite`.  
- Or adjust that constant to the real path.

***

## 4. Next steps (exporting to MariaDB)

For the POC, this meta box proves that:

- The cosine‑based related posts are reasonable.  
- The mapping from `post_id -> related_post_id` is correct.

For production:

- You’ll likely periodically copy `post_related` from SQLite to a MariaDB table (same schema), then adapt the plugin to query that table instead of SQLite (via `$wpdb`).  
- The UI code (meta box) will remain identical; only the data source changes from PDO/SQLite to `$wpdb`/MariaDB.

If you want, in a next step I can give you:

- A small PHP/CLI or Python script to migrate `post_related` from SQLite to MariaDB (WP’s DB).  
- The plugin variant that uses `$wpdb` instead of SQLite.

## PROMPT_2
Redo the plugin as I do not want to use the SQLite but the MariaDB (WP’s DB) and I want also to be able to update easily my list of related posts because i will redo the compute of the similarity one in a while so I want the easiest way to update the content contained into the SQLite so what is the best way to do it, put all the rows into the plugin for instance or leverage on a .sql export but I want to have the content installed right away when i install the plugin and be able to update the content.

So what is the most pragmatic strategy in order to migrate content, use .sql, use a .txt, use a .csv, I want to be able to change the content source and have a procedure to reload the new data if I redo the similarity procedure. I want the most secure one, for instance I upload a new file in the plugin and the plugin drops the table and creates a new table and reloads the new content, you have the point .
The plugin variant must be using `$wpdb` instead of SQLite as I will install the plugin in a wp in production. I want to be able to install and uninstall the plugin as much as I want.

## OUTPUT_2
You’ll get the most pragmatic, production‑friendly setup if you:

- Store everything in a dedicated MySQL/MariaDB table.  
- Ship the initial data as a CSV inside the plugin.  
- Provide an admin page with a file upload to “re‑load” a new CSV: plugin drops/truncates the table and bulk‑inserts the new rows.  

Below is a complete plugin that:

- Creates a `wp_related_posts_embeddings` table on activation.  
- Lets you import a CSV of `(post_id, related_post_id, similarity, rank)` from `/wp-admin` (settings page).  
- Uses `$wpdb` to show related posts in a meta box on the post edit screen.  
- Drops the table on uninstall (clean uninstall).

Adjust naming and paths as you like.

***

## 1. Expected CSV format

For imports, use a simple CSV with header:

```text
post_id,related_post_id,similarity,rank
13091,12927,0.5533628113550911,1
13091,12840,0.5273974579326484,2
13091,12947,0.5141183899494592,3
13091,12815,0.47802840827521753,4
13091,11616,0.4754158172759728,5
...
```

You can generate this CSV from your SQLite database in your Python pipeline.

***

## 2. Plugin file

Create `wp-content/plugins/wp-related-embeddings/wp-related-embeddings.php` and paste:

```php
<?php
/**
 * Plugin Name: WP Related Posts via Embeddings (DB)
 * Description: Stores and displays related posts (via embeddings) in a custom MySQL table, with CSV import.
 * Version: 0.1.0
 * Author: Your Name
 * Text Domain: wp-related-embeddings-db
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * CONFIG
 */

define( 'WP_RE_EMB_PLUGIN_VERSION', '0.1.0' );

/**
 * Get full table name for related embeddings.
 */
function wp_re_emb_table_name() {
    global $wpdb;
    return $wpdb->prefix . 'related_posts_embeddings';
}


/**
 * ACTIVATION: create the custom table.
 */
function wp_re_emb_activate() {
    global $wpdb;

    $table_name = wp_re_emb_table_name();

    $charset_collate = $wpdb->get_charset_collate();

    $sql = "
        CREATE TABLE {$table_name} (
            id BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
            post_id BIGINT(20) UNSIGNED NOT NULL,
            related_post_id BIGINT(20) UNSIGNED NOT NULL,
            similarity DOUBLE NOT NULL,
            rank INT(11) NOT NULL,
            PRIMARY KEY  (id),
            KEY post_id (post_id),
            KEY related_post_id (related_post_id)
        ) {$charset_collate};
    ";

    require_once ABSPATH . 'wp-admin/includes/upgrade.php';
    dbDelta( $sql );
}
register_activation_hook( __FILE__, 'wp_re_emb_activate' );


/**
 * UNINSTALL: drop the custom table.
 *
 * Note: this runs only on plugin uninstall, not on deactivation.
 */
function wp_re_emb_uninstall() {
    global $wpdb;

    $table_name = wp_re_emb_table_name();
    $wpdb->query( "DROP TABLE IF EXISTS {$table_name}" );
}
register_uninstall_hook( __FILE__, 'wp_re_emb_uninstall' );


/**
 * Fetch related posts from MySQL for a given post_id.
 *
 * Returns an array of arrays:
 * [
 *   [
 *     'related_post_id' => int,
 *     'similarity'      => float,
 *     'rank'            => int,
 *   ],
 *   ...
 * ]
 */
function wp_re_emb_get_related_from_db( $post_id, $limit = 10 ) {
    global $wpdb;

    $table_name = wp_re_emb_table_name();

    $sql = $wpdb->prepare(
        "SELECT related_post_id, similarity, rank
         FROM {$table_name}
         WHERE post_id = %d
         ORDER BY rank ASC
         LIMIT %d",
        $post_id,
        $limit
    );

    $rows = $wpdb->get_results( $sql, ARRAY_A );

    $out = array();
    if ( $rows ) {
        foreach ( $rows as $row ) {
            $out[] = array(
                'related_post_id' => (int) $row['related_post_id'],
                'similarity'      => (float) $row['similarity'],
                'rank'            => (int) $row['rank'],
            );
        }
    }

    return $out;
}


/**
 * Meta box: display related posts on the post edit screen.
 */
function wp_re_emb_render_meta_box( WP_Post $post ) {
    $post_id      = $post->ID;
    $max_related  = 10; // change here if you want another default
    $related_rows = wp_re_emb_get_related_from_db( $post_id, $max_related );

    echo '<p>';
    esc_html_e( 'These related posts are computed offline from embeddings and stored in the WordPress database.', 'wp-related-embeddings-db' );
    echo '</p>';

    if ( empty( $related_rows ) ) {
        echo '<p><em>' . esc_html__( 'No related posts found for this post.', 'wp-related-embeddings-db' ) . '</em></p>';
        return;
    }

    echo '<table class="widefat fixed striped">';
    echo '<thead><tr>';
    echo '<th>' . esc_html__( 'Rank', 'wp-related-embeddings-db' ) . '</th>';
    echo '<th>' . esc_html__( 'Related Post', 'wp-related-embeddings-db' ) . '</th>';
    echo '<th>' . esc_html__( 'Similarity', 'wp-related-embeddings-db' ) . '</th>';
    echo '</tr></thead>';
    echo '<tbody>';

    foreach ( $related_rows as $row ) {
        $rel_id   = $row['related_post_id'];
        $rank     = $row['rank'];
        $sim      = $row['similarity'];
        $rel_post = get_post( $rel_id );

        echo '<tr>';

        echo '<td>' . esc_html( $rank ) . '</td>';

        echo '<td>';
        if ( $rel_post instanceof WP_Post ) {
            $title = get_the_title( $rel_post );
            $url   = get_edit_post_link( $rel_post );
            echo '<a href="' . esc_url( $url ) . '">';
            echo esc_html( sprintf( '%d – %s', $rel_id, $title ) );
            echo '</a>';
        } else {
            echo esc_html( sprintf( 'Post ID %d (not found)', $rel_id ) );
        }
        echo '</td>';

        echo '<td>' . esc_html( number_format( $sim, 3 ) ) . '</td>';

        echo '</tr>';
    }

    echo '</tbody>';
    echo '</table>';
}


/**
 * Register meta box on post edit screens.
 */
function wp_re_emb_add_meta_box() {
    add_meta_box(
        'wp_related_embeddings_meta_box',
        __( 'Related Posts (Embeddings)', 'wp-related-embeddings-db' ),
        'wp_re_emb_render_meta_box',
        'post',
        'side',
        'default'
    );
}
add_action( 'add_meta_boxes', 'wp_re_emb_add_meta_box' );


/**
 * ADMIN: Settings page for CSV import (upload + reload).
 *
 * Strategy:
 * - In /wp-admin, show a page under "Settings -> Related Embeddings".
 * - Allow uploading a CSV file.
 * - On submit, truncate the custom table and bulk-insert new rows.
 */
function wp_re_emb_admin_menu() {
    add_options_page(
        __( 'Related Embeddings', 'wp-related-embeddings-db' ),
        __( 'Related Embeddings', 'wp-related-embeddings-db' ),
        'manage_options',
        'wp-related-embeddings',
        'wp_re_emb_render_settings_page'
    );
}
add_action( 'admin_menu', 'wp_re_emb_admin_menu' );


/**
 * Handle CSV import: truncate table and insert new rows.
 */
function wp_re_emb_handle_csv_import() {
    if ( ! current_user_can( 'manage_options' ) ) {
        return;
    }

    if ( ! isset( $_POST['wp_re_emb_import_nonce'] ) || ! wp_verify_nonce( $_POST['wp_re_emb_import_nonce'], 'wp_re_emb_import_csv' ) ) {
        return;
    }

    if ( empty( $_FILES['wp_re_emb_csv']['tmp_name'] ) ) {
        add_settings_error(
            'wp_re_emb_messages',
            'wp_re_emb_no_file',
            __( 'No CSV file uploaded.', 'wp-related-embeddings-db' ),
            'error'
        );
        return;
    }

    $file = $_FILES['wp_re_emb_csv']['tmp_name'];

    // Basic MIME / extension check could be added if you want.
    $handle = fopen( $file, 'r' );
    if ( ! $handle ) {
        add_settings_error(
            'wp_re_emb_messages',
            'wp_re_emb_file_open_error',
            __( 'Could not open uploaded file.', 'wp-related-embeddings-db' ),
            'error'
        );
        return;
    }

    global $wpdb;
    $table_name = wp_re_emb_table_name();

    // Truncate table (fast, clean).
    $wpdb->query( "TRUNCATE TABLE {$table_name}" );

    // Read header.
    $header = fgetcsv( $handle );
    if ( ! $header ) {
        fclose( $handle );
        add_settings_error(
            'wp_re_emb_messages',
            'wp_re_emb_bad_header',
            __( 'CSV file is empty or has no header.', 'wp-related-embeddings-db' ),
            'error'
        );
        return;
    }

    // Expect columns: post_id, related_post_id, similarity, rank (in any order).
    $index = array(
        'post_id'         => array_search( 'post_id', $header ),
        'related_post_id' => array_search( 'related_post_id', $header ),
        'similarity'      => array_search( 'similarity', $header ),
        'rank'            => array_search( 'rank', $header ),
    );

    foreach ( $index as $key => $pos ) {
        if ( $pos === false ) {
            fclose( $handle );
            add_settings_error(
                'wp_re_emb_messages',
                'wp_re_emb_missing_column_' . $key,
                sprintf(
                    /* translators: 1: column name */
                    __( 'CSV missing required column: %s', 'wp-related-embeddings-db' ),
                    esc_html( $key )
                ),
                'error'
            );
            return;
        }
    }

    $inserted = 0;

    while ( ( $row = fgetcsv( $handle ) ) !== false ) {
        // Skip empty rows.
        if ( count( $row ) < 4 ) {
            continue;
        }

        $post_id         = isset( $row[ $index['post_id'] ] ) ? (int) $row[ $index['post_id'] ] : 0;
        $related_post_id = isset( $row[ $index['related_post_id'] ] ) ? (int) $row[ $index['related_post_id'] ] : 0;
        $similarity      = isset( $row[ $index['similarity'] ] ) ? (float) $row[ $index['similarity'] ] : 0.0;
        $rank            = isset( $row[ $index['rank'] ] ) ? (int) $row[ $index['rank'] ] : 0;

        if ( $post_id <= 0 || $related_post_id <= 0 || $rank <= 0 ) {
            continue;
        }

        $wpdb->insert(
            $table_name,
            array(
                'post_id'         => $post_id,
                'related_post_id' => $related_post_id,
                'similarity'      => $similarity,
                'rank'            => $rank,
            ),
            array( '%d', '%d', '%f', '%d' )
        );

        if ( ! empty( $wpdb->insert_id ) ) {
            $inserted++;
        }
    }

    fclose( $handle );

    add_settings_error(
        'wp_re_emb_messages',
        'wp_re_emb_import_success',
        sprintf(
            __( 'Imported %d related rows (table truncated before import).', 'wp-related-embeddings-db' ),
            $inserted
        ),
        'updated'
    );
}


/**
 * Settings page HTML.
 */
function wp_re_emb_render_settings_page() {
    if ( isset( $_POST['wp_re_emb_import_submit'] ) ) {
        wp_re_emb_handle_csv_import();
    }

    settings_errors( 'wp_re_emb_messages' );

    ?>
    <div class="wrap">
        <h1><?php esc_html_e( 'Related Posts Embeddings Import', 'wp-related-embeddings-db' ); ?></h1>

        <p>
            <?php esc_html_e( 'Upload a CSV file with columns: post_id, related_post_id, similarity, rank. The plugin will TRUNCATE the custom table and load the new data.', 'wp-related-embeddings-db' ); ?>
        </p>

        <form method="post" enctype="multipart/form-data">
            <?php wp_nonce_field( 'wp_re_emb_import_csv', 'wp_re_emb_import_nonce' ); ?>

            <table class="form-table" role="presentation">
                <tr>
                    <th scope="row">
                        <label for="wp_re_emb_csv"><?php esc_html_e( 'CSV File', 'wp-related-embeddings-db' ); ?></label>
                    </th>
                    <td>
                        <input type="file" id="wp_re_emb_csv" name="wp_re_emb_csv" accept=".csv,text/csv" />
                    </td>
                </tr>
            </table>

            <?php submit_button( __( 'Import CSV (truncate & reload)', 'wp-related-embeddings-db' ), 'primary', 'wp_re_emb_import_submit' ); ?>
        </form>
    </div>
    <?php
}
```

***

## 3. Workflow for updating related posts

1. Run your Python pipeline that recomputes similarity and writes `post_related` in SQLite.  
2. Export `post_related` to a CSV with columns `post_id, related_post_id, similarity, rank`.  
3. Go to `Settings → Related Embeddings` in WP admin.  
4. Upload the CSV and click “Import CSV (truncate & reload)”.  
   - Plugin truncates the custom table.  
   - Inserts all new rows.  
5. On any post edit screen, the meta box shows the updated related posts list.

This is:

- Safe (CSV is easy to inspect and version).  
- Repeatable (you can recompute similarity whenever you want).  
- Clean (plugin activation creates the table, uninstall drops it; no manual SQL needed). [developer.wordpress](https://developer.wordpress.org/plugins/creating-tables-with-plugins/)


## PROMPT_2

As a python expert, create a script named `010_parsing_posts_similarity_sqlite_export_sqlite_csv.py` that will perform :
1. Run your Python pipeline that recomputes similarity and writes `post_related` in SQLite.  
2. Export `post_related` to a CSV with columns `post_id, related_post_id, similarity, rank`.

So I can have a safe (CSV is easy to inspect and version) and repeatable (you can recompute similarity whenever you want).  




## OUTPUT_2

You can wrap everything in one script that:

- Recomputes embeddings and similarities (using your existing pipeline patterns).  
- Writes `post_related` into a SQLite DB.  
- Exports `post_related` to a CSV with the right header and columns.

Here is `010_parsing_posts_similarity_sqlite_export_sqlite_csv.py` as a self‑contained script, assuming:

- JSON input: `sample_posts_2020_to_2025.json`.  
- SQLite DB: `related_posts_embeddings_settings.sqlite`.  
- CSV output: `related_posts_embeddings.csv`.  

You can adjust these at the top.

```python
"""
POINT_6 helper - Recompute similarity, store in SQLite, export to CSV.

File: 010_parsing_posts_similarity_sqlite_export_sqlite_csv.py

This script:
1. Loads WP posts from JSON.
2. Builds embeddings with sentence-transformers.
3. Computes cosine similarity between posts, keeps top-K per post
   with a similarity threshold.
4. Stores results in a SQLite database (post_embeddings + post_related).
5. Exports post_related to a CSV: post_id, related_post_id, similarity, rank.

This CSV can then be imported into the WP plugin's MySQL table.
"""

import csv
import json
import logging
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

import html
import re

import numpy as np
from sentence_transformers import SentenceTransformer  # type: ignore[import]


# --------------------------------------------------------------------
# Logging
# --------------------------------------------------------------------

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)


# --------------------------------------------------------------------
# CONFIGURATION - edit as needed
# --------------------------------------------------------------------

@dataclass
class EmbeddingConfig:
    # Input WP JSON (same file you used for previous scripts)
    wp_json_path: Path = Path("sample_posts_2020_to_2025.json")

    # Embedding
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    batch_size: int = 32
    max_chars: int = 4000
    include_slug: bool = False
    normalize_embeddings: bool = True

    # SQLite DB for intermediate storage
    sqlite_path: Path = Path("related_posts_embeddings_settings.sqlite")

    # Similarity settings
    post_number_against: int = 10    # top-K per post
    threshold_for_similarity: float = 0.40  # minimum cosine similarity

    # CSV output
    csv_output_path: Path = Path("related_posts_embeddings.csv")


# --------------------------------------------------------------------
# Data model & JSON loading
# --------------------------------------------------------------------

@dataclass
class ParsedPost:
    id: int
    title_rendered: str
    content: str
    slug: Optional[str] = None


def load_posts_from_json(path: Path) -> List[ParsedPost]:
    logger.info("Loading posts from JSON: %s", path)

    with path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    def get_nested(mapping, path_seq, default=None):
        current = mapping
        for key in path_seq:
            if not isinstance(current, dict) or key not in current:
                return default
            current = current[key]
        return current

    posts: List[ParsedPost] = []
    for item in raw:
        posts.append(
            ParsedPost(
                id=int(item["id"]),
                title_rendered=str(get_nested(item, ["title", "rendered"], "")),
                content=str(get_nested(item, ["content", "rendered"], "")),
                slug=str(get_nested(item, ["slug"], "")),
            )
        )

    logger.info("Loaded %d posts", len(posts))
    return posts


# --------------------------------------------------------------------
# Pre-processing
# --------------------------------------------------------------------

_HTML_TAG_RE = re.compile(r"<[^>]+>")


def strip_html_tags(text: str) -> str:
    unescaped = html.unescape(text)
    return _HTML_TAG_RE.sub("", unescaped)


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def build_post_text(
    post: ParsedPost,
    max_chars: Optional[int] = None,
    include_slug: bool = False,
) -> str:
    title = normalize_whitespace(post.title_rendered)
    content_raw = post.content or ""
    content_clean = normalize_whitespace(strip_html_tags(content_raw))

    parts: List[str] = []

    if title:
        parts.append(f"TITLE: {title}")

    if content_clean:
        parts.append(f"CONTENT: {content_clean}")

    if include_slug and post.slug:
        parts.append(f"SLUG: {post.slug}")

    full_text = "\n\n".join(parts)

    if max_chars is not None and len(full_text) > max_chars:
        full_text = full_text[:max_chars]

    return full_text


# --------------------------------------------------------------------
# Embeddings with batching
# --------------------------------------------------------------------

_model: Optional[SentenceTransformer] = None


def get_embedding_model(model_name: str) -> SentenceTransformer:
    global _model
    if _model is None:
        logger.info("Loading embedding model: %s", model_name)
        _model = SentenceTransformer(model_name)
    return _model


def iter_batches(items: Sequence[ParsedPost], batch_size: int):
    if batch_size <= 0:
        raise ValueError("batch_size must be > 0")

    n = len(items)
    for start in range(0, n, batch_size):
        end = start + batch_size
        yield items[start:end]


EmbeddingVector = List[float]
PostEmbedding = Tuple[int, EmbeddingVector]


def embed_posts_batched(
    posts: Sequence[ParsedPost],
    config: EmbeddingConfig,
) -> List[PostEmbedding]:
    if not posts:
        logger.warning("No posts to embed")
        return []

    model = get_embedding_model(config.embedding_model_name)
    results: List[PostEmbedding] = []

    logger.info(
        "Embedding %d posts with batch_size=%d, max_chars=%d, include_slug=%s, normalize=%s",
        len(posts),
        config.batch_size,
        config.max_chars,
        config.include_slug,
        config.normalize_embeddings,
    )

    for batch_posts in iter_batches(posts, config.batch_size):
        texts = [
            build_post_text(
                p,
                max_chars=config.max_chars,
                include_slug=config.include_slug,
            )
            for p in batch_posts
        ]

        embeddings = model.encode(
            texts,
            normalize_embeddings=config.normalize_embeddings,
        )
        emb_arr = np.asarray(embeddings)

        for post, vec in zip(batch_posts, emb_arr):
            results.append((post.id, vec.astype(float).tolist()))

    logger.info("Finished embedding %d posts", len(results))
    return results


# --------------------------------------------------------------------
# Similarity computation
# --------------------------------------------------------------------

def compute_similarity_top_k(
    embeddings: List[PostEmbedding],
    top_k: int,
    similarity_threshold: float,
) -> List[Tuple[int, List[Tuple[int, float]]]]:
    """
    Returns:
        list of (post_id, [(related_post_id, similarity), ...])
    """
    if not embeddings:
        return []

    post_ids = [pid for pid, _ in embeddings]
    mat = np.asarray([vec for _, vec in embeddings], dtype=float)  # (N, D)

    norms = np.linalg.norm(mat, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    mat_norm = mat / norms

    sim_matrix = mat_norm @ mat_norm.T  # (N, N)

    n = sim_matrix.shape[0]
    all_results: List[Tuple[int, List[Tuple[int, float]]]] = []

    logger.info(
        "Computing similarities with top_k=%d, threshold_for_similarity=%.3f",
        top_k,
        similarity_threshold,
    )

    for i in range(n):
        sim_matrix[i, i] = -np.inf

        idx = np.argsort(sim_matrix[i])[-top_k:][::-1]

        related: List[Tuple[int, float]] = []
        for j in idx:
            score = float(sim_matrix[i, j])
            if score < similarity_threshold:
                continue
            rel_post_id = post_ids[j]
            related.append((rel_post_id, score))

        all_results.append((post_ids[i], related))

    return all_results


# --------------------------------------------------------------------
# SQLite storage for post_embeddings + post_related
# --------------------------------------------------------------------

def init_sqlite(db_path: Path) -> sqlite3.Connection:
    logger.info("Initializing SQLite DB at %s", db_path)
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS post_embeddings (
            post_id INTEGER PRIMARY KEY,
            embedding_json TEXT NOT NULL
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS post_related (
            post_id INTEGER NOT NULL,
            related_post_id INTEGER NOT NULL,
            similarity REAL NOT NULL,
            rank INTEGER NOT NULL,
            PRIMARY KEY (post_id, related_post_id)
        )
        """
    )

    conn.commit()
    return conn


def store_embeddings(conn: sqlite3.Connection, embeddings: List[PostEmbedding]) -> None:
    logger.info("Storing %d embeddings into SQLite", len(embeddings))
    cur = conn.cursor()

    rows = [
        (post_id, json.dumps(vec))
        for post_id, vec in embeddings
    ]

    cur.executemany(
        """
        INSERT OR REPLACE INTO post_embeddings (post_id, embedding_json)
        VALUES (?, ?)
        """,
        rows,
    )
    conn.commit()


def store_related(
    conn: sqlite3.Connection,
    related_by_post: List[Tuple[int, List[Tuple[int, float]]]],
) -> None:
    logger.info("Storing related posts into SQLite")
    cur = conn.cursor()

    to_insert: List[Tuple[int, int, float, int]] = []

    for post_id, related_list in related_by_post:
        for rank, (rel_id, score) in enumerate(related_list, start=1):
            to_insert.append((post_id, rel_id, score, rank))

    cur.executemany(
        """
        INSERT OR REPLACE INTO post_related (post_id, related_post_id, similarity, rank)
        VALUES (?, ?, ?, ?)
        """,
        to_insert,
    )
    conn.commit()


# --------------------------------------------------------------------
# CSV export from SQLite
# --------------------------------------------------------------------

def export_post_related_to_csv(
    conn: sqlite3.Connection,
    csv_path: Path,
) -> None:
    logger.info("Exporting post_related to CSV at %s", csv_path)

    cur = conn.cursor()
    cur.execute(
        """
        SELECT post_id, related_post_id, similarity, rank
        FROM post_related
        ORDER BY post_id ASC, rank ASC
        """
    )
    rows = cur.fetchall()

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["post_id", "related_post_id", "similarity", "rank"])
        for row in rows:
            writer.writerow(row)

    logger.info("Exported %d rows to %s", len(rows), csv_path)


# --------------------------------------------------------------------
# Main pipeline
# --------------------------------------------------------------------

def main() -> None:
    config = EmbeddingConfig()
    logger.info("Effective configuration: %s", config)

    # 1. Load posts
    posts = load_posts_from_json(config.wp_json_path)

    # 2. Embed posts
    embeddings = embed_posts_batched(posts, config)

    # 3. Compute similarity
    related_by_post = compute_similarity_top_k(
        embeddings,
        top_k=config.post_number_against,
        similarity_threshold=config.threshold_for_similarity,
    )

    # 4. Store in SQLite
    conn = init_sqlite(config.sqlite_path)
    try:
        store_embeddings(conn, embeddings)
        store_related(conn, related_by_post)

        # 5. Export post_related to CSV
        export_post_related_to_csv(conn, config.csv_output_path)
    finally:
        conn.close()

    logger.info("Done. CSV ready at %s", config.csv_output_path)


if __name__ == "__main__":
    main()
```

Usage:

```bash
conda activate tags_treatment
python 010_parsing_posts_similarity_sqlite_export_sqlite_csv.py
```

You’ll get:

- Updated `related_posts_embeddings_settings.sqlite` with fresh `post_related`.  
- A CSV `related_posts_embeddings.csv` ready to import into your WP plugin’s MySQL table. [stackoverflow](https://stackoverflow.com/questions/10522830/how-to-export-sqlite-to-csv-in-python-without-being-formatted-as-a-list)



## INPUT_2

Can you rewrite the script with the name `bf_wp_related_embeddings_db.php`. The DB is called `related_posts_embeddings_settings_csv.sqlite` and the csv `related_posts_embeddings_settings_csv.csv` make it as variables into the plugin so I can update it easily. I have tried to install the first version of the plugin, I got the message "Imported 0 related rows (table truncated before import)." and the csv was not empty, can you fox it.

- extract from `related_posts_embeddings_settings_csv.csv`
``` csv
post_id,related_post_id,similarity,rank
11463,13091,0.4403083154651628,1
11485,11874,0.43104943526829276,1
etc...
```

## OUTPUT_3

You’re right to want this as simple and deterministic as possible: plugin uses MariaDB only, and you update data by uploading a new CSV that truncates and reloads the table.

Below is a revised plugin as a single file named `bf_wp_related_embeddings_db.php` with:

- Clear constants for CSV file name and (if you still want it) the old SQLite name.  
- Robust CSV import that should correctly handle your example CSV.  
- Creation/drop of the custom table on activation/uninstall.  
- Meta box using `$wpdb` only.

You’ll typically:

1. Run your Python script to regenerate `related_posts_embeddings_settings_csv.csv`.  
2. Go to `Settings → Related Embeddings` in WP, upload that CSV, and reload the table.

***

## 1. Plugin file: `bf_wp_related_embeddings_db.php`

Place this in `wp-content/plugins/bf_wp_related_embeddings_db/bf_wp_related_embeddings_db.php`:

```php
<?php
/**
 * Plugin Name: BF Related Posts via Embeddings (DB)
 * Description: Stores and displays related posts (via embeddings) in a custom MySQL table, with CSV import.
 * Version: 0.2.0
 * Author: Your Name
 * Text Domain: bf-wp-related-embeddings-db
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * CONFIG
 *
 * Edit these if you change file naming conventions.
 */

// Default CSV filename you generate in your Python pipeline
define( 'BF_RE_EMB_DEFAULT_CSV_FILENAME', 'related_posts_embeddings_settings_csv.csv' );

// (Optional, for reference) the SQLite filename your pipeline uses internally
define( 'BF_RE_EMB_DEFAULT_SQLITE_FILENAME', 'related_posts_embeddings_settings_csv.sqlite' );


/**
 * Helper: full table name.
 */
function bf_re_emb_table_name() {
    global $wpdb;
    return $wpdb->prefix . 'related_posts_embeddings';
}


/**
 * ACTIVATION: create custom table.
 */
function bf_re_emb_activate() {
    global $wpdb;

    $table_name      = bf_re_emb_table_name();
    $charset_collate = $wpdb->get_charset_collate();

    $sql = "
        CREATE TABLE {$table_name} (
            id BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
            post_id BIGINT(20) UNSIGNED NOT NULL,
            related_post_id BIGINT(20) UNSIGNED NOT NULL,
            similarity DOUBLE NOT NULL,
            rank INT(11) NOT NULL,
            PRIMARY KEY  (id),
            KEY post_id (post_id),
            KEY related_post_id (related_post_id)
        ) {$charset_collate};
    ";

    require_once ABSPATH . 'wp-admin/includes/upgrade.php';
    dbDelta( $sql );
}
register_activation_hook( __FILE__, 'bf_re_emb_activate' );


/**
 * UNINSTALL: drop custom table.
 */
function bf_re_emb_uninstall() {
    global $wpdb;

    $table_name = bf_re_emb_table_name();
    $wpdb->query( "DROP TABLE IF EXISTS {$table_name}" );
}
register_uninstall_hook( __FILE__, 'bf_re_emb_uninstall' );


/**
 * Fetch related posts from MySQL for a given post_id.
 */
function bf_re_emb_get_related_from_db( $post_id, $limit = 10 ) {
    global $wpdb;

    $table_name = bf_re_emb_table_name();

    $sql = $wpdb->prepare(
        "SELECT related_post_id, similarity, rank
         FROM {$table_name}
         WHERE post_id = %d
         ORDER BY rank ASC
         LIMIT %d",
        $post_id,
        $limit
    );

    $rows = $wpdb->get_results( $sql, ARRAY_A );

    $out = array();
    if ( $rows ) {
        foreach ( $rows as $row ) {
            $out[] = array(
                'related_post_id' => (int) $row['related_post_id'],
                'similarity'      => (float) $row['similarity'],
                'rank'            => (int) $row['rank'],
            );
        }
    }

    return $out;
}


/**
 * Meta box: display related posts on post edit screen.
 */
function bf_re_emb_render_meta_box( WP_Post $post ) {
    $post_id      = $post->ID;
    $max_related  = 10; // adjust if needed
    $related_rows = bf_re_emb_get_related_from_db( $post_id, $max_related );

    echo '<p>';
    esc_html_e(
        'These related posts are computed offline from embeddings and stored in the WordPress database (custom table).',
        'bf-wp-related-embeddings-db'
    );
    echo '</p>';

    if ( empty( $related_rows ) ) {
        echo '<p><em>' . esc_html__(
            'No related posts found for this post.',
            'bf-wp-related-embeddings-db'
        ) . '</em></p>';
        return;
    }

    echo '<table class="widefat fixed striped">';
    echo '<thead><tr>';
    echo '<th>' . esc_html__( 'Rank', 'bf-wp-related-embeddings-db' ) . '</th>';
    echo '<th>' . esc_html__( 'Related Post', 'bf-wp-related-embeddings-db' ) . '</th>';
    echo '<th>' . esc_html__( 'Similarity', 'bf-wp-related-embeddings-db' ) . '</th>';
    echo '</tr></thead>';
    echo '<tbody>';

    foreach ( $related_rows as $row ) {
        $rel_id   = $row['related_post_id'];
        $rank     = $row['rank'];
        $sim      = $row['similarity'];
        $rel_post = get_post( $rel_id );

        echo '<tr>';

        echo '<td>' . esc_html( $rank ) . '</td>';

        echo '<td>';
        if ( $rel_post instanceof WP_Post ) {
            $title = get_the_title( $rel_post );
            $url   = get_edit_post_link( $rel_post );
            echo '<a href="' . esc_url( $url ) . '">';
            echo esc_html( sprintf( '%d – %s', $rel_id, $title ) );
            echo '</a>';
        } else {
            echo esc_html( sprintf( 'Post ID %d (not found)', $rel_id ) );
        }
        echo '</td>';

        echo '<td>' . esc_html( number_format( $sim, 3 ) ) . '</td>';

        echo '</tr>';
    }

    echo '</tbody>';
    echo '</table>';
}


/**
 * Register meta box on posts.
 */
function bf_re_emb_add_meta_box() {
    add_meta_box(
        'bf_related_embeddings_meta_box',
        __( 'Related Posts (Embeddings)', 'bf-wp-related-embeddings-db' ),
        'bf_re_emb_render_meta_box',
        'post',
        'side',
        'default'
    );
}
add_action( 'add_meta_boxes', 'bf_re_emb_add_meta_box' );


/**
 * ADMIN MENU: settings page for CSV import.
 */
function bf_re_emb_admin_menu() {
    add_options_page(
        __( 'Related Embeddings', 'bf-wp-related-embeddings-db' ),
        __( 'Related Embeddings', 'bf-wp-related-embeddings-db' ),
        'manage_options',
        'bf-wp-related-embeddings-db',
        'bf_re_emb_render_settings_page'
    );
}
add_action( 'admin_menu', 'bf_re_emb_admin_menu' );


/**
 * Handle CSV import.
 *
 * Expect header row: post_id,related_post_id,similarity,rank
 * Example:
 * 11463,13091,0.4403083154651628,1
 * 11485,11874,0.43104943526829276,1
 */
function bf_re_emb_handle_csv_import() {
    if ( ! current_user_can( 'manage_options' ) ) {
        return;
    }

    if ( ! isset( $_POST['bf_re_emb_import_nonce'] ) || ! wp_verify_nonce( $_POST['bf_re_emb_import_nonce'], 'bf_re_emb_import_csv' ) ) {
        return;
    }

    if ( empty( $_FILES['bf_re_emb_csv']['tmp_name'] ) ) {
        add_settings_error(
            'bf_re_emb_messages',
            'bf_re_emb_no_file',
            __( 'No CSV file uploaded.', 'bf-wp-related-embeddings-db' ),
            'error'
        );
        return;
    }

    $tmp_name = $_FILES['bf_re_emb_csv']['tmp_name'];

    $handle = fopen( $tmp_name, 'r' );
    if ( ! $handle ) {
        add_settings_error(
            'bf_re_emb_messages',
            'bf_re_emb_file_open_error',
            __( 'Could not open uploaded file.', 'bf-wp-related-embeddings-db' ),
            'error'
        );
        return;
    }

    global $wpdb;
    $table_name = bf_re_emb_table_name();

    // TRUNCATE table first (safe + predictable).
    $wpdb->query( "TRUNCATE TABLE {$table_name}" );

    // Read header row.
    $header = fgetcsv( $handle );
    if ( ! $header ) {
        fclose( $handle );
        add_settings_error(
            'bf_re_emb_messages',
            'bf_re_emb_bad_header',
            __( 'CSV file is empty or has no header.', 'bf-wp-related-embeddings-db' ),
            'error'
        );
        return;
    }

    // Normalize header values (strip BOM, trim, lowercase).
    $normalized_header = array();
    foreach ( $header as $col ) {
        $col = preg_replace( '/^\xEF\xBB\xBF/', '', $col ); // remove UTF-8 BOM if present
        $normalized_header[] = strtolower( trim( $col ) );
    }

    $index = array(
        'post_id'         => array_search( 'post_id', $normalized_header, true ),
        'related_post_id' => array_search( 'related_post_id', $normalized_header, true ),
        'similarity'      => array_search( 'similarity', $normalized_header, true ),
        'rank'            => array_search( 'rank', $normalized_header, true ),
    );

    foreach ( $index as $key => $pos ) {
        if ( $pos === false ) {
            fclose( $handle );
            add_settings_error(
                'bf_re_emb_messages',
                'bf_re_emb_missing_column_' . $key,
                sprintf(
                    __( 'CSV missing required column: %s', 'bf-wp-related-embeddings-db' ),
                    esc_html( $key )
                ),
                'error'
            );
            return;
        }
    }

    $inserted = 0;

    // Process each data row.
    while ( ( $row = fgetcsv( $handle ) ) !== false ) {
        // Skip completely empty rows.
        if ( empty( array_filter( $row, 'strlen' ) ) ) {
            continue;
        }

        $post_id         = isset( $row[ $index['post_id'] ] ) ? (int) $row[ $index['post_id'] ] : 0;
        $related_post_id = isset( $row[ $index['related_post_id'] ] ) ? (int) $row[ $index['related_post_id'] ] : 0;
        $similarity      = isset( $row[ $index['similarity'] ] ) ? (float) $row[ $index['similarity'] ] : 0.0;
        $rank            = isset( $row[ $index['rank'] ] ) ? (int) $row[ $index['rank'] ] : 0;

        if ( $post_id <= 0 || $related_post_id <= 0 || $rank <= 0 ) {
            // Ignore invalid rows but keep going.
            continue;
        }

        $result = $wpdb->insert(
            $table_name,
            array(
                'post_id'         => $post_id,
                'related_post_id' => $related_post_id,
                'similarity'      => $similarity,
                'rank'            => $rank,
            ),
            array( '%d', '%d', '%f', '%d' )
        );

        if ( $result !== false ) {
            $inserted++;
        }
    }

    fclose( $handle );

    add_settings_error(
        'bf_re_emb_messages',
        'bf_re_emb_import_success',
        sprintf(
            __( 'Imported %d related rows (table truncated before import).', 'bf-wp-related-embeddings-db' ),
            $inserted
        ),
        'updated'
    );
}


/**
 * Settings page HTML (CSV upload).
 */
function bf_re_emb_render_settings_page() {
    if ( isset( $_POST['bf_re_emb_import_submit'] ) ) {
        bf_re_emb_handle_csv_import();
    }

    settings_errors( 'bf_re_emb_messages' );

    ?>
    <div class="wrap">
        <h1><?php esc_html_e( 'Related Posts Embeddings Import', 'bf-wp-related-embeddings-db' ); ?></h1>

        <p>
            <?php esc_html_e(
                'Upload a CSV file with columns: post_id, related_post_id, similarity, rank. The plugin will TRUNCATE the custom table and load the new data.',
                'bf-wp-related-embeddings-db'
            ); ?>
        </p>

        <p>
            <?php
            printf(
                /* translators: 1: default CSV filename */
                esc_html__(
                    'Typical file name from your pipeline: %s',
                    'bf-wp-related-embeddings-db'
                ),
                '<code>' . esc_html( BF_RE_EMB_DEFAULT_CSV_FILENAME ) . '</code>'
            );
            ?>
        </p>

        <form method="post" enctype="multipart/form-data">
            <?php wp_nonce_field( 'bf_re_emb_import_csv', 'bf_re_emb_import_nonce' ); ?>

            <table class="form-table" role="presentation">
                <tr>
                    <th scope="row">
                        <label for="bf_re_emb_csv"><?php esc_html_e( 'CSV File', 'bf-wp-related-embeddings-db' ); ?></label>
                    </th>
                    <td>
                        <input type="file" id="bf_re_emb_csv" name="bf_re_emb_csv" accept=".csv,text/csv" />
                    </td>
                </tr>
            </table>

            <?php submit_button(
                __( 'Import CSV (truncate & reload)', 'bf-wp-related-embeddings-db' ),
                'primary',
                'bf_re_emb_import_submit'
            ); ?>
        </form>
    </div>
    <?php
}
```

Key fixes for the “Imported 0 rows” issue:

- Header handling strips a UTF‑8 BOM and lowercases/trims column names, so `post_id,related_post_id,similarity,rank` will be recognized even if editors add BOM/spacing. [stackoverflow](https://stackoverflow.com/questions/74072615/wordpress-plugin-unable-to-import-csv-data-to-custom-plugin-table)
- The importer skips only truly invalid/empty rows and counts `insert` results, not `$wpdb->insert_id`, which can stay 0 after `TRUNCATE` with some DB engines. [wp-kama](https://wp-kama.com/function/wpdb-insert)

***

## 2. How to use this in your workflow

1. Regenerate CSV from Python using your script (e.g. `related_posts_embeddings_settings_csv.csv`).  
2. In WordPress admin:
   - Activate “BF Related Posts via Embeddings (DB)”.  
   - Go to Settings → Related Embeddings.  
   - Upload the CSV and import.  
3. On a post edit screen:
   - Look at the “Related Posts (Embeddings)” meta box on the side.  
   - You should see the rows from your CSV for that `post_id`, sorted by rank and showing similarity.

When you recompute similarity:

- Generate a new CSV with the same header.  
- Re‑upload it; plugin truncates and reloads the table, giving you a clean, repeatable process.


## PROMPT_3
I should see the table `wp_related_posts_embeddings` in phpmyadmin when I install the plugin and when I uninstall the plugin it should drop the table `wp_related_posts_embeddings` right ? 

## OUTPUT_3

Yes, that’s exactly how this plugin is designed to behave:

- On activation, it calls `bf_re_emb_activate()`, which runs `dbDelta()` with a `CREATE TABLE` statement for:

  ```php
  $table_name = $wpdb->prefix . 'related_posts_embeddings';
  ```

  On a default install where the table prefix is `wp_`, that becomes `wp_related_posts_embeddings`. [developer.wordpress](https://developer.wordpress.org/plugins/creating-tables-with-plugins/)

- On uninstall (using “Delete” in the Plugins screen, not just “Deactivate”), it calls `bf_re_emb_uninstall()`, which executes:

  ```php
  $wpdb->query( "DROP TABLE IF EXISTS {$table_name}" );
  ```

  That drops `wp_related_posts_embeddings` from MariaDB. [tutorials24x7](https://www.tutorials24x7.com/wordpress/create-db-table-on-activating-wordpress-plugin)

So in phpMyAdmin:

- After activation: you should see `wp_related_posts_embeddings` (empty until you import a CSV).  
- After uninstall: that table should no longer exist.

## PROMPT_4
There is not import (Imported 0 related rows (table truncated before import) and not table creation avalaible in phpmyadmin. I am using docker I should not ba force to restart phpmyadmin.





## OUTPUT_4

Two separate things are failing here: table creation on activation and CSV import. Both must work before you see data in phpMyAdmin and in the meta box.

I’ll show you:

- A corrected version of `bf_wp_related_embeddings_db.php` with explicit constants for your SQLite/CSV naming, and safer activation/import logic.  
- What to check step‑by‑step so you can see exactly where it fails.

***

## 1. Updated plugin skeleton (same file name)

File: `wp-content/plugins/bf_wp_related_embeddings_db/bf_wp_related_embeddings_db.php`

```php
<?php
/**
 * Plugin Name: BF Related Posts via Embeddings (DB)
 * Description: Stores and displays related posts (via embeddings) in a custom MySQL table, with CSV import.
 * Version: 0.2.1
 * Author: Your Name
 * Text Domain: bf-wp-related-embeddings-db
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * CONFIG
 *
 * Update these if you change your file naming.
 */

// The CSV you generate from Python, e.g. 010_* script.
define( 'BF_RE_EMB_DEFAULT_CSV_FILENAME', 'related_posts_embeddings_settings_csv.csv' );

// Mentioned for reference, not used in this plugin:
define( 'BF_RE_EMB_DEFAULT_SQLITE_FILENAME', 'related_posts_embeddings_settings_csv.sqlite' );


/**
 * Return full table name, with WP prefix.
 */
function bf_re_emb_table_name() {
    global $wpdb;
    return $wpdb->prefix . 'related_posts_embeddings';
}


/**
 * ACTIVATION: create custom table via dbDelta.
 */
function bf_re_emb_activate() {
    global $wpdb;

    $table_name      = bf_re_emb_table_name();
    $charset_collate = $wpdb->get_charset_collate();

    $sql = "CREATE TABLE {$table_name} (
        id BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
        post_id BIGINT(20) UNSIGNED NOT NULL,
        related_post_id BIGINT(20) UNSIGNED NOT NULL,
        similarity DOUBLE NOT NULL,
        rank INT(11) NOT NULL,
        PRIMARY KEY  (id),
        KEY post_id (post_id),
        KEY related_post_id (related_post_id)
    ) {$charset_collate};";

    require_once ABSPATH . 'wp-admin/includes/upgrade.php';

    // For debugging, you can temporarily uncomment the next line:
    // error_log( 'bf_re_emb_activate SQL: ' . $sql );

    dbDelta( $sql );
}
register_activation_hook( __FILE__, 'bf_re_emb_activate' );


/**
 * UNINSTALL: drop custom table completely.
 */
function bf_re_emb_uninstall() {
    global $wpdb;

    $table_name = bf_re_emb_table_name();
    $wpdb->query( "DROP TABLE IF EXISTS {$table_name}" );
}
register_uninstall_hook( __FILE__, 'bf_re_emb_uninstall' );


/**
 * Fetch related posts from DB (for post edit meta box & frontend use).
 */
function bf_re_emb_get_related_from_db( $post_id, $limit = 10 ) {
    global $wpdb;

    $table_name = bf_re_emb_table_name();

    $sql = $wpdb->prepare(
        "SELECT related_post_id, similarity, rank
         FROM {$table_name}
         WHERE post_id = %d
         ORDER BY rank ASC
         LIMIT %d",
        $post_id,
        $limit
    );

    $rows = $wpdb->get_results( $sql, ARRAY_A );

    $out = array();
    if ( $rows ) {
        foreach ( $rows as $row ) {
            $out[] = array(
                'related_post_id' => (int) $row['related_post_id'],
                'similarity'      => (float) $row['similarity'],
                'rank'            => (int) $row['rank'],
            );
        }
    }

    return $out;
}


/**
 * Meta box: display related posts in post edit.
 */
function bf_re_emb_render_meta_box( WP_Post $post ) {
    $post_id      = $post->ID;
    $max_related  = 10;
    $related_rows = bf_re_emb_get_related_from_db( $post_id, $max_related );

    echo '<p>';
    esc_html_e(
        'These related posts are computed offline from embeddings and stored in the WordPress database (custom table).',
        'bf-wp-related-embeddings-db'
    );
    echo '</p>';

    if ( empty( $related_rows ) ) {
        echo '<p><em>' . esc_html__(
            'No related posts found for this post.',
            'bf-wp-related-embeddings-db'
        ) . '</em></p>';
        return;
    }

    echo '<table class="widefat fixed striped">';
    echo '<thead><tr>';
    echo '<th>' . esc_html__( 'Rank', 'bf-wp-related-embeddings-db' ) . '</th>';
    echo '<th>' . esc_html__( 'Related Post', 'bf-wp-related-embeddings-db' ) . '</th>';
    echo '<th>' . esc_html__( 'Similarity', 'bf-wp-related-embeddings-db' ) . '</th>';
    echo '</tr></thead>';
    echo '<tbody>';

    foreach ( $related_rows as $row ) {
        $rel_id   = $row['related_post_id'];
        $rank     = $row['rank'];
        $sim      = $row['similarity'];
        $rel_post = get_post( $rel_id );

        echo '<tr>';

        echo '<td>' . esc_html( $rank ) . '</td>';

        echo '<td>';
        if ( $rel_post instanceof WP_Post ) {
            $title = get_the_title( $rel_post );
            $url   = get_edit_post_link( $rel_post );
            echo '<a href="' . esc_url( $url ) . '">';
            echo esc_html( sprintf( '%d – %s', $rel_id, $title ) );
            echo '</a>';
        } else {
            echo esc_html( sprintf( 'Post ID %d (not found)', $rel_id ) );
        }
        echo '</td>';

        echo '<td>' . esc_html( number_format( $sim, 3 ) ) . '</td>';

        echo '</tr>';
    }

    echo '</tbody>';
    echo '</table>';
}


/**
 * Register meta box.
 */
function bf_re_emb_add_meta_box() {
    add_meta_box(
        'bf_related_embeddings_meta_box',
        __( 'Related Posts (Embeddings)', 'bf-wp-related-embeddings-db' ),
        'bf_re_emb_render_meta_box',
        'post',
        'side',
        'default'
    );
}
add_action( 'add_meta_boxes', 'bf_re_emb_add_meta_box' );


/**
 * Admin menu: CSV import page.
 */
function bf_re_emb_admin_menu() {
    add_options_page(
        __( 'Related Embeddings', 'bf-wp-related-embeddings-db' ),
        __( 'Related Embeddings', 'bf-wp-related-embeddings-db' ),
        'manage_options',
        'bf-wp-related-embeddings-db',
        'bf_re_emb_render_settings_page'
    );
}
add_action( 'admin_menu', 'bf_re_emb_admin_menu' );


/**
 * CSV import handler.
 */
function bf_re_emb_handle_csv_import() {
    if ( ! current_user_can( 'manage_options' ) ) {
        return;
    }

    if ( ! isset( $_POST['bf_re_emb_import_nonce'] ) || ! wp_verify_nonce( $_POST['bf_re_emb_import_nonce'], 'bf_re_emb_import_csv' ) ) {
        return;
    }

    if ( empty( $_FILES['bf_re_emb_csv']['tmp_name'] ) ) {
        add_settings_error(
            'bf_re_emb_messages',
            'bf_re_emb_no_file',
            __( 'No CSV file uploaded.', 'bf-wp-related-embeddings-db' ),
            'error'
        );
        return;
    }

    $tmp_name = $_FILES['bf_re_emb_csv']['tmp_name'];

    // Quick sanity check: log path & size.
    error_log( sprintf(
        '[bf_wp_related_embeddings_db] Uploaded CSV: %s (size: %d bytes)',
        $tmp_name,
        filesize( $tmp_name )
    ) );

    $handle = fopen( $tmp_name, 'r' );
    if ( ! $handle ) {
        add_settings_error(
            'bf_re_emb_messages',
            'bf_re_emb_file_open_error',
            __( 'Could not open uploaded file.', 'bf-wp-related-embeddings-db' ),
            'error'
        );
        return;
    }

    global $wpdb;
    $table_name = bf_re_emb_table_name();

    // Ensure table exists (if activation somehow failed).
    bf_re_emb_activate();

    // Truncate table.
    $wpdb->query( "TRUNCATE TABLE {$table_name}" );

    // Header row.
    $header = fgetcsv( $handle );
    if ( ! $header ) {
        fclose( $handle );
        add_settings_error(
            'bf_re_emb_messages',
            'bf_re_emb_bad_header',
            __( 'CSV file is empty or has no header.', 'bf-wp-related-embeddings-db' ),
            'error'
        );
        return;
    }

    // Normalize header.
    $normalized_header = array();
    foreach ( $header as $col ) {
        $col = preg_replace( '/^\xEF\xBB\xBF/', '', $col ); // UTF-8 BOM
        $normalized_header[] = strtolower( trim( $col ) );
    }

    $index = array(
        'post_id'         => array_search( 'post_id', $normalized_header, true ),
        'related_post_id' => array_search( 'related_post_id', $normalized_header, true ),
        'similarity'      => array_search( 'similarity', $normalized_header, true ),
        'rank'            => array_search( 'rank', $normalized_header, true ),
    );

    foreach ( $index as $key => $pos ) {
        if ( $pos === false ) {
            fclose( $handle );
            add_settings_error(
                'bf_re_emb_messages',
                'bf_re_emb_missing_column_' . $key,
                sprintf(
                    __( 'CSV missing required column: %s', 'bf-wp-related-embeddings-db' ),
                    esc_html( $key )
                ),
                'error'
            );
            return;
        }
    }

    $inserted = 0;

    while ( ( $row = fgetcsv( $handle ) ) !== false ) {
        if ( empty( array_filter( $row, 'strlen' ) ) ) {
            continue;
        }

        $post_id         = isset( $row[ $index['post_id'] ] ) ? (int) $row[ $index['post_id'] ] : 0;
        $related_post_id = isset( $row[ $index['related_post_id'] ] ) ? (int) $row[ $index['related_post_id'] ] : 0;
        $similarity      = isset( $row[ $index['similarity'] ] ) ? (float) $row[ $index['similarity'] ] : 0.0;
        $rank            = isset( $row[ $index['rank'] ] ) ? (int) $row[ $index['rank'] ] : 0;

        if ( $post_id <= 0 || $related_post_id <= 0 || $rank <= 0 ) {
            continue;
        }

        $result = $wpdb->insert(
            $table_name,
            array(
                'post_id'         => $post_id,
                'related_post_id' => $related_post_id,
                'similarity'      => $similarity,
                'rank'            => $rank,
            ),
            array( '%d', '%d', '%f', '%d' )
        );

        if ( $result !== false ) {
            $inserted++;
        }
    }

    fclose( $handle );

    add_settings_error(
        'bf_re_emb_messages',
        'bf_re_emb_import_success',
        sprintf(
            __( 'Imported %d related rows (table truncated before import).', 'bf-wp-related-embeddings-db' ),
            $inserted
        ),
        'updated'
    );
}


/**
 * Settings page.
 */
function bf_re_emb_render_settings_page() {
    if ( isset( $_POST['bf_re_emb_import_submit'] ) ) {
        bf_re_emb_handle_csv_import();
    }

    settings_errors( 'bf_re_emb_messages' );

    ?>
    <div class="wrap">
        <h1><?php esc_html_e( 'Related Posts Embeddings Import', 'bf-wp-related-embeddings-db' ); ?></h1>

        <p>
            <?php esc_html_e(
                'Upload a CSV file with columns: post_id, related_post_id, similarity, rank. The plugin will TRUNCATE the custom table and load the new data.',
                'bf-wp-related-embeddings-db'
            ); ?>
        </p>

        <p>
            <?php
            printf(
                esc_html__(
                    'Typical file name from your pipeline: %s',
                    'bf-wp-related-embeddings-db'
                ),
                '<code>' . esc_html( BF_RE_EMB_DEFAULT_CSV_FILENAME ) . '</code>'
            );
            ?>
        </p>

        <form method="post" enctype="multipart/form-data">
            <?php wp_nonce_field( 'bf_re_emb_import_csv', 'bf_re_emb_import_nonce' ); ?>

            <table class="form-table" role="presentation">
                <tr>
                    <th scope="row">
                        <label for="bf_re_emb_csv"><?php esc_html_e( 'CSV File', 'bf-wp-related-embeddings-db' ); ?></label>
                    </th>
                    <td>
                        <input type="file" id="bf_re_emb_csv" name="bf_re_emb_csv" accept=".csv,text/csv" />
                    </td>
                </tr>
            </table>

            <?php submit_button(
                __( 'Import CSV (truncate & reload)', 'bf-wp-related-embeddings-db' ),
                'primary',
                'bf_re_emb_import_submit'
            ); ?>
        </form>
    </div>
    <?php
}
```

***

## 2. Things to verify in Docker/phpMyAdmin

1. **Activation actually runs**

   - Deactivate and **delete** the plugin.  
   - Re‑upload / copy the folder.  
   - Activate the plugin again in `/wp-admin/plugins.php`.  
   - If activation fails, you’ll see a PHP error.  
   - If it succeeds, check phpMyAdmin for a table named `<prefix>_related_posts_embeddings` (often `wp_related_posts_embeddings`). [developer.wordpress](https://developer.wordpress.org/plugins/creating-tables-with-plugins/)

2. **Table appears without restarting phpMyAdmin**

   - phpMyAdmin shows live schema; you do not need to restart it.  
   - If the table is not there, either:
     - `dbDelta` is not running (activation hook not bound to the correct file), or  
     - the SQL fails (check `error_log` in the container). [stackoverflow](https://stackoverflow.com/questions/34300767/wordpress-plugin-table-cannot-create-with-dbdelta-although-sql-is-correct)

3. **CSV import path and size**

   - When you upload the CSV, in `wp-content/debug.log` (or container logs) you should see something like:

     ```text
     [bf_wp_related_embeddings_db] Uploaded CSV: /tmp/phpxxxxxx (size: 12345 bytes)
     ```

   - If size is 0, the upload itself failed (PHP upload size, rights, etc.). [stackoverflow](https://stackoverflow.com/questions/5593473/how-to-upload-and-parse-a-csv-file-in-php)

4. **Header exactly matches**

   Your extract:

   ```csv
   post_id,related_post_id,similarity,rank
   11463,13091,0.4403083154651628,1
   11485,11874,0.43104943526829276,1
   ```

   Matches what the importer expects. If there is any BOM or spaces, the normalisation will handle it.

5. **Check table content directly**

   In phpMyAdmin (or `wp db cli`):

   ```sql
   SELECT COUNT(*) FROM wp_related_posts_embeddings;
   SELECT * FROM wp_related_posts_embeddings ORDER BY post_id, rank LIMIT 10;
   ```

   If the `Imported X related rows` message says X > 0 but table is empty, we have a DB user permission issue; you’d then see errors in the PHP logs. [reddit](https://www.reddit.com/r/Wordpress/comments/635pja/dbdelta_creates_the_new_database_tables_but_not/)

If after this you still see `Imported 0 related rows` for your sample CSV, paste a few complete rows (as saved on disk) and we can tighten the CSV parsing even more.

## PROMPT_5
I still see `Imported 0 related rows` for your sample CSV, paste a few complete rows (as saved on disk) and we can tighten the CSV parsing even more.

```csv
post_id,related_post_id,similarity,rank
11463,13091,0.4403083154651628,1
11485,11874,0.43104943526829276,1
11485,11962,0.4189954422008453,2
11485,11972,0.4039861695118566,3
11485,12532,0.4035007365782019,4
11485,11563,0.40167606766660674,5
11510,12492,0.5946657418609803,1
11510,11654,0.5606656322744209,2
11510,11563,0.4909766761699117,3
11510,12569,0.4072429259313907,4
11510,12512,0.40576783347884193,5
11563,12492,0.6628788898527752,1
11563,12747,0.5654787780065247,2
11563,12512,0.5453232268028783,3
11563,12379,0.5097684952544108,4
11563,12127,0.5017527606943333,5
11563,11510,0.4909766761699117,6
11563,12678,0.4804783835188834,7
11563,11874,0.467647157654702,8
11563,12569,0.45771819110340467,9
11563,11972,0.44179237106515734,10
11587,12368,0.42708275775467625,1
11616,12239,0.5229391184820468,1
11616,13091,0.4754158172759728,2
11616,11874,0.4500395256818022,3
11616,12840,0.4299234219765935,4
11616,12368,0.4076586831337427,5
11616,11631,0.4046560694727777,6
11616,12452,0.4030858909746263,7
11631,11563,0.4311683639602131,1
11631,12452,0.4084738062526736,2
11631,11616,0.4046560694727777,3
11654,12492,0.6218383452563602,1
11654,11510,0.5606656322744209,2
11833,12512,0.4571098405177574,1
11833,12747,0.4394962545052498,2
11833,12492,0.40218625420320914,3
11874,11972,0.7120723471379131,1
11874,11915,0.4962569075360273,2
11874,12015,0.4825709068812126,3
11874,12859,0.47710020722583457,4
11874,12512,0.4752350120316727,5
11874,12127,0.46918892130785295,6
11874,11563,0.467647157654702,7
11874,12774,0.4665435432270018,8
11874,12239,0.4623050660750667,9
11874,12747,0.45104832367963393,10
11915,11874,0.4962569075360273,1
11915,11962,0.4788851540525495,2
11915,12015,0.4663465595147701,3
11915,13091,0.4438368249919609,4
11915,12368,0.4223868276933214,5
11962,12368,0.4856320842234806,1
11962,11915,0.4788851540525495,2
11962,12840,0.46106342785576204,3
11962,11485,0.4189954422008453,4
11962,13091,0.4044603622461457,5
11962,12219,0.40431059743403164,6
11972,11874,0.7120723471379131,1
11972,12512,0.5415416924020944,2
11972,12058,0.518038139285722,3
11972,12127,0.4724090215378773,4
11972,12859,0.4673456827218972,5
11972,11563,0.44179237106515734,6
11972,12532,0.4387090792212161,7
11972,12651,0.43536409979132584,8
11972,12015,0.43425439230494106,9
11972,12740,0.43396374152220685,10
12015,12740,0.48334890796363805,1
12015,11874,0.4825709068812126,2
12015,12532,0.46955575377339603,3
12015,11915,0.4663465595147701,4
12015,11972,0.43425439230494106,5
12015,12058,0.41633733536189754,6
12015,12127,0.4119595617838703,7
12058,11972,0.518038139285722,1
12058,12740,0.46990316149463746,2
12058,12015,0.41633733536189754,3
12058,11874,0.4006436363122585,4
12127,12747,0.5118196767839546,1
12127,11563,0.5017527606943333,2
12127,11972,0.4724090215378773,3
12127,11874,0.46918892130785295,4
12127,12569,0.43862813052130745,5
12127,12492,0.43379534706191597,6
12127,12678,0.42227175652505883,7
12127,12379,0.4176014765414854,8
12127,12015,0.4119595617838703,9
12127,13042,0.4089967083257911,10
12192,12433,0.5204795020916991,1
12192,12239,0.5036572507731674,2
12192,12329,0.43573967202826003,3
12219,12368,0.4546614996173403,1
12219,12379,0.42858467038914566,2
12219,13091,0.42839611291619106,3
12219,13042,0.40575618792593093,4
12219,11962,0.40431059743403164,5
12219,12239,0.4009264032823989,6
12239,11616,0.5229391184820468,1
12239,12192,0.5036572507731674,2
12239,11874,0.4623050660750667,3
12239,12433,0.4193887888124529,4
12239,12368,0.40835225421734167,5
12239,12219,0.4009264032823989,6
12329,12433,0.5508911168367226,1
12329,12192,0.43573967202826003,2
12368,11962,0.4856320842234806,1
12368,12219,0.4546614996173403,2
12368,11587,0.42708275775467625,3
12368,11915,0.4223868276933214,4
12368,12239,0.40835225421734167,5
12368,11616,0.4076586831337427,6
12379,12727,0.5420752051324067,1
12379,11563,0.5097684952544108,2
12379,12569,0.4809879046406002,3
12379,12747,0.46513379988541986,4
12379,12458,0.4622182127152267,5
12379,13091,0.4608174038344029,6
12379,12927,0.43302022772200954,7
12379,12219,0.42858467038914566,8
12379,12127,0.4176014765414854,9
12379,12888,0.410000391523102,10
12433,12329,0.5508911168367226,1
12433,12192,0.5204795020916991,2
12433,12727,0.44549085911052033,3
12433,12239,0.4193887888124529,4
12433,12747,0.4129979845194534,5
12433,12379,0.4047284636573712,6
12452,12458,0.6973248315795265,1
12452,12840,0.5652317939781907,2
12452,12927,0.5161966780030965,3
12452,12947,0.4764936943966306,4
12452,13091,0.47159116958575914,5
12452,12747,0.432679659523097,6
12452,13008,0.4137099594201219,7
12452,11631,0.4084738062526736,8
12452,11616,0.4030858909746263,9
12452,11563,0.4013785110792991,10
12458,12452,0.6973248315795265,1
12458,12927,0.5623917779132578,2
12458,12774,0.5269153188832214,3
12458,12747,0.5141295432332893,4
12458,12569,0.5076963930249228,5
12458,13091,0.46692043408436623,6
12458,12379,0.4622182127152267,7
12458,13008,0.44401987025745043,8
12458,13070,0.43527418986466226,9
12458,12840,0.4334454109477793,10
12492,11563,0.6628788898527752,1
12492,11654,0.6218383452563602,2
12492,11510,0.5946657418609803,3
12492,12747,0.5161028353730187,4
12492,12512,0.49091594850325965,5
12492,12569,0.47831239240820794,6
12492,12127,0.43379534706191597,7
12492,12927,0.42675480392104426,8
12492,12678,0.40683240108167623,9
12492,11833,0.40218625420320914,10
12512,12532,0.6732468622679352,1
12512,12651,0.5567158831325085,2
12512,12569,0.5463136756031075,3
12512,11563,0.5453232268028783,4
12512,11972,0.5415416924020944,5
12512,12678,0.5279321737796846,6
12512,12859,0.504106461342852,7
12512,12747,0.49351715734558715,8
12512,12492,0.49091594850325965,9
12512,11874,0.4752350120316727,10
12532,12512,0.6732468622679352,1
12532,12015,0.46955575377339603,2
12532,12707,0.4633370045224793,3
12532,12859,0.4499972024354528,4
12532,12569,0.4499318716425578,5
12532,12747,0.4445961176350901,6
12532,11972,0.4387090792212161,7
12532,12678,0.4350373474423306,8
12532,12651,0.4349150951141774,9
12532,11485,0.4035007365782019,10
12569,12747,0.6673123462291636,1
12569,12774,0.580223319093879,2
12569,12707,0.5556050854948199,3
12569,12727,0.5509434426877741,4
12569,12512,0.5463136756031075,5
12569,12678,0.5417663581176515,6
12569,12888,0.5191388875803605,7
12569,12458,0.5076963930249228,8
12569,12927,0.5000542936608071,9
12569,12379,0.4809879046406002,10
12651,12512,0.5567158831325085,1
12651,12859,0.4775788024174758,2
12651,12707,0.47081477059280796,3
12651,12569,0.4383050844851572,4
12651,11972,0.43536409979132584,5
12651,12532,0.4349150951141774,6
12651,13008,0.40906003838660787,7
12678,12569,0.5417663581176515,1
12678,12747,0.5319928618821826,2
12678,12512,0.5279321737796846,3
12678,11563,0.4804783835188834,4
12678,12774,0.4611513495053698,5
12678,12532,0.4350373474423306,6
12678,12127,0.42227175652505883,7
12678,12492,0.40683240108167623,8
12678,12707,0.4009818469159661,9
12707,12569,0.5556050854948199,1
12707,12747,0.5321045808979593,2
12707,12727,0.5267064114441827,3
12707,12774,0.4961353068341296,4
12707,12512,0.47213676503782,5
12707,12651,0.47081477059280796,6
12707,12888,0.469615696759843,7
12707,12532,0.4633370045224793,8
12707,13051,0.4268409508331624,9
12707,12910,0.42643227638016984,10
12727,12569,0.5509434426877741,1
12727,12379,0.5420752051324067,2
12727,12707,0.5267064114441827,3
12727,12747,0.4720641490655679,4
12727,12433,0.44549085911052033,5
12727,12774,0.4374403680970216,6
12727,12888,0.4164465989694378,7
12727,11563,0.4083303000858315,8
12740,12015,0.48334890796363805,1
12740,12058,0.46990316149463746,2
12740,11972,0.43396374152220685,3
12740,12512,0.4049613692272023,4
12747,12774,0.687130233999764,1
12747,12569,0.6673123462291636,2
12747,12927,0.5888113744354069,3
12747,11563,0.5654787780065247,4
12747,12707,0.5321045808979593,5
12747,12678,0.5319928618821826,6
12747,12888,0.5287666545175826,7
12747,12492,0.5161028353730187,8
12747,12458,0.5141295432332893,9
12747,12127,0.5118196767839546,10
12774,12747,0.687130233999764,1
12774,12569,0.580223319093879,2
12774,12927,0.5488058668626085,3
12774,12458,0.5269153188832214,4
12774,13070,0.5259421528377681,5
12774,12707,0.4961353068341296,6
12774,12888,0.48912952202825144,7
12774,11874,0.4665435432270018,8
12774,13051,0.4613829206933494,9
12774,12678,0.4611513495053698,10
12815,13008,0.4834871881770946,1
12815,13091,0.47802840827521753,2
12815,13070,0.455780881944843,3
12815,12774,0.44523428812507293,4
12815,12927,0.4092021542750092,5
12815,12840,0.40377726924286195,6
12840,12452,0.5652317939781907,1
12840,13091,0.5273974579326484,2
12840,12927,0.49812608760970994,3
12840,12947,0.46648757620973125,4
12840,11962,0.46106342785576204,5
12840,12774,0.4561096892341941,6
12840,12458,0.4334454109477793,7
12840,11616,0.4299234219765935,8
12840,13070,0.4291612627564655,9
12840,11874,0.4264343461473315,10
12859,12512,0.504106461342852,1
12859,12651,0.4775788024174758,2
12859,11874,0.47710020722583457,3
12859,11972,0.4673456827218972,4
12859,12532,0.4499972024354528,5
12859,12774,0.44654699312787854,6
12859,12569,0.4353038912860719,7
12859,12747,0.4291076131969625,8
12888,13051,0.6371061167178792,1
12888,12747,0.5287666545175826,2
12888,12910,0.5252598517392723,3
12888,12569,0.5191388875803605,4
12888,12774,0.48912952202825144,5
12888,12707,0.469615696759843,6
12888,12927,0.4450925951596426,7
12888,12458,0.4181590972751119,8
12888,13070,0.4174183968674735,9
12888,12727,0.4164465989694378,10
12910,12888,0.5252598517392723,1
12910,13051,0.5246526653903218,2
12910,12707,0.42643227638016984,3
12910,12774,0.42614045784604665,4
12927,12747,0.5888113744354069,1
12927,12458,0.5623917779132578,2
12927,13091,0.5533628113550911,3
12927,12774,0.5488058668626085,4
12927,12452,0.5161966780030965,5
12927,13070,0.5020753504323374,6
12927,12569,0.5000542936608071,7
12927,12840,0.49812608760970994,8
12927,13008,0.4918992171727813,9
12927,12947,0.4879097598961757,10
12947,13091,0.5141183899494592,1
12947,12927,0.4879097598961757,2
12947,12452,0.4764936943966306,3
12947,13070,0.4699905907141321,4
12947,12840,0.46648757620973125,5
12947,13008,0.4432903973917827,6
12947,13042,0.43218068961488393,7
12947,12458,0.41023389334174665,8
13008,12927,0.4918992171727813,1
13008,12815,0.4834871881770946,2
13008,13070,0.4698633817927474,3
13008,13091,0.4448108094922877,4
13008,12458,0.44401987025745043,5
13008,12947,0.4432903973917827,6
13008,13042,0.4389970422875304,7
13008,12569,0.4268748402835369,8
13008,12774,0.4142292211017818,9
13008,12452,0.4137099594201219,10
13042,12927,0.48201001755670697,1
13042,13008,0.4389970422875304,2
13042,12947,0.43218068961488393,3
13042,13091,0.4296975534327731,4
13042,11563,0.4185621024096637,5
13042,12747,0.41263109991368024,6
13042,12127,0.4089967083257911,7
13042,13070,0.40855149187533124,8
13042,12219,0.40575618792593093,9
13042,12458,0.40260765498934026,10
13051,12888,0.6371061167178792,1
13051,12910,0.5246526653903218,2
13051,12774,0.4613829206933494,3
13051,12747,0.4332128922050067,4
13051,12707,0.4268409508331624,5
13070,12774,0.5259421528377681,1
13070,12927,0.5020753504323374,2
13070,12947,0.4699905907141321,3
13070,13008,0.4698633817927474,4
13070,12815,0.455780881944843,5
13070,12747,0.4387808630190759,6
13070,12458,0.43527418986466226,7
13070,12840,0.4291612627564655,8
13070,12888,0.4174183968674735,9
13070,13042,0.40855149187533124,10
13091,12927,0.5533628113550911,1
13091,12840,0.5273974579326484,2
13091,12947,0.5141183899494592,3
13091,12815,0.47802840827521753,4
13091,11616,0.4754158172759728,5
13091,12452,0.47159116958575914,6
13091,12458,0.46692043408436623,7
13091,12379,0.4608174038344029,8
13091,13008,0.4448108094922877,9
13091,11915,0.4438368249919609,10

```

## OUTPUT_5
The CSV itself is fine; the issue is either header matching or the table not existing when you import. Here’s a minimal, stricter version of the plugin that:

- Ensures the table is created before import.  
- Logs file size and the first data row.  
- Uses very explicit header parsing that will work with your sample.  

You’ll be able to:

- See `wp_related_posts_embeddings` in phpMyAdmin after activation.  
- Import your CSV and see a non‑zero “Imported X rows” message.  

Below is a simplified `bf_wp_related_embeddings_db.php` you can drop in and test.

```php
<?php
/**
 * Plugin Name: BF Related Posts via Embeddings (DB)
 * Description: Stores and displays related posts (via embeddings) in a custom MySQL table, with CSV import.
 * Version: 0.3.0
 * Author: Your Name
 * Text Domain: bf-wp-related-embeddings-db
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * CONFIG
 */

define( 'BF_RE_EMB_DEFAULT_CSV_FILENAME', 'related_posts_embeddings_settings_csv.csv' );

/**
 * Helper: full table name.
 */
function bf_re_emb_table_name() {
    global $wpdb;
    return $wpdb->prefix . 'related_posts_embeddings';
}

/**
 * ACTIVATION: create custom table.
 */
function bf_re_emb_activate() {
    global $wpdb;

    $table_name      = bf_re_emb_table_name();
    $charset_collate = $wpdb->get_charset_collate();

    $sql = "CREATE TABLE {$table_name} (
        id BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
        post_id BIGINT(20) UNSIGNED NOT NULL,
        related_post_id BIGINT(20) UNSIGNED NOT NULL,
        similarity DOUBLE NOT NULL,
        rank INT(11) NOT NULL,
        PRIMARY KEY  (id),
        KEY post_id (post_id),
        KEY related_post_id (related_post_id)
    ) {$charset_collate};";

    require_once ABSPATH . 'wp-admin/includes/upgrade.php';
    dbDelta( $sql );
}
register_activation_hook( __FILE__, 'bf_re_emb_activate' );

/**
 * UNINSTALL: drop custom table.
 */
function bf_re_emb_uninstall() {
    global $wpdb;

    $table_name = bf_re_emb_table_name();
    $wpdb->query( "DROP TABLE IF EXISTS {$table_name}" );
}
register_uninstall_hook( __FILE__, 'bf_re_emb_uninstall' );

/**
 * Fetch related posts from DB.
 */
function bf_re_emb_get_related_from_db( $post_id, $limit = 10 ) {
    global $wpdb;

    $table_name = bf_re_emb_table_name();

    $sql = $wpdb->prepare(
        "SELECT related_post_id, similarity, rank
         FROM {$table_name}
         WHERE post_id = %d
         ORDER BY rank ASC
         LIMIT %d",
        $post_id,
        $limit
    );

    $rows = $wpdb->get_results( $sql, ARRAY_A );

    $out = array();
    if ( $rows ) {
        foreach ( $rows as $row ) {
            $out[] = array(
                'related_post_id' => (int) $row['related_post_id'],
                'similarity'      => (float) $row['similarity'],
                'rank'            => (int) $row['rank'],
            );
        }
    }

    return $out;
}

/**
 * Meta box: show related posts in post edit screen.
 */
function bf_re_emb_render_meta_box( WP_Post $post ) {
    $post_id      = $post->ID;
    $max_related  = 10;
    $related_rows = bf_re_emb_get_related_from_db( $post_id, $max_related );

    echo '<p>';
    esc_html_e(
        'These related posts are computed offline from embeddings and stored in the WordPress database (custom table).',
        'bf-wp-related-embeddings-db'
    );
    echo '</p>';

    if ( empty( $related_rows ) ) {
        echo '<p><em>' . esc_html__(
            'No related posts found for this post.',
            'bf-wp-related-embeddings-db'
        ) . '</em></p>';
        return;
    }

    echo '<table class="widefat fixed striped">';
    echo '<thead><tr>';
    echo '<th>' . esc_html__( 'Rank', 'bf-wp-related-embeddings-db' ) . '</th>';
    echo '<th>' . esc_html__( 'Related Post', 'bf-wp-related-embeddings-db' ) . '</th>';
    echo '<th>' . esc_html__( 'Similarity', 'bf-wp-related-embeddings-db' ) . '</th>';
    echo '</tr></thead>';
    echo '<tbody>';

    foreach ( $related_rows as $row ) {
        $rel_id   = $row['related_post_id'];
        $rank     = $row['rank'];
        $sim      = $row['similarity'];
        $rel_post = get_post( $rel_id );

        echo '<tr>';

        echo '<td>' . esc_html( $rank ) . '</td>';

        echo '<td>';
        if ( $rel_post instanceof WP_Post ) {
            $title = get_the_title( $rel_post );
            $url   = get_edit_post_link( $rel_post );
            echo '<a href="' . esc_url( $url ) . '">';
            echo esc_html( sprintf( '%d – %s', $rel_id, $title ) );
            echo '</a>';
        } else {
            echo esc_html( sprintf( 'Post ID %d (not found)', $rel_id ) );
        }
        echo '</td>';

        echo '<td>' . esc_html( number_format( $sim, 3 ) ) . '</td>';

        echo '</tr>';
    }

    echo '</tbody>';
    echo '</table>';
}

/**
 * Register meta box.
 */
function bf_re_emb_add_meta_box() {
    add_meta_box(
        'bf_related_embeddings_meta_box',
        __( 'Related Posts (Embeddings)', 'bf-wp-related-embeddings-db' ),
        'bf_re_emb_render_meta_box',
        'post',
        'side',
        'default'
    );
}
add_action( 'add_meta_boxes', 'bf_re_emb_add_meta_box' );

/**
 * Admin menu.
 */
function bf_re_emb_admin_menu() {
    add_options_page(
        __( 'Related Embeddings', 'bf-wp-related-embeddings-db' ),
        __( 'Related Embeddings', 'bf-wp-related-embeddings-db' ),
        'manage_options',
        'bf-wp-related-embeddings-db',
        'bf_re_emb_render_settings_page'
    );
}
add_action( 'admin_menu', 'bf_re_emb_admin_menu' );

/**
 * CSV import handler (tighter version).
 */
function bf_re_emb_handle_csv_import() {
    if ( ! current_user_can( 'manage_options' ) ) {
        return;
    }

    if ( ! isset( $_POST['bf_re_emb_import_nonce'] ) || ! wp_verify_nonce( $_POST['bf_re_emb_import_nonce'], 'bf_re_emb_import_csv' ) ) {
        return;
    }

    if ( empty( $_FILES['bf_re_emb_csv']['tmp_name'] ) ) {
        add_settings_error(
            'bf_re_emb_messages',
            'bf_re_emb_no_file',
            __( 'No CSV file uploaded.', 'bf-wp-related-embeddings-db' ),
            'error'
        );
        return;
    }

    $tmp_name = $_FILES['bf_re_emb_csv']['tmp_name'];

    // Basic logging to debug in Docker.
    error_log( sprintf(
        '[bf_wp_related_embeddings_db] Uploaded CSV: %s (size: %d bytes)',
        $tmp_name,
        @filesize( $tmp_name )
    ) );

    $handle = fopen( $tmp_name, 'r' );
    if ( ! $handle ) {
        add_settings_error(
            'bf_re_emb_messages',
            'bf_re_emb_file_open_error',
            __( 'Could not open uploaded file.', 'bf-wp-related-embeddings-db' ),
            'error'
        );
        return;
    }

    global $wpdb;
    $table_name = bf_re_emb_table_name();

    // Ensure table exists in case activation didn't run.
    bf_re_emb_activate();

    // Truncate table.
    $wpdb->query( "TRUNCATE TABLE {$table_name}" );

    // Header row.
    $header = fgetcsv( $handle );
    if ( ! $header ) {
        fclose( $handle );
        add_settings_error(
            'bf_re_emb_messages',
            'bf_re_emb_bad_header',
            __( 'CSV file is empty or has no header.', 'bf-wp-related-embeddings-db' ),
            'error'
        );
        return;
    }

    // Normalise header.
    $normalized_header = array();
    foreach ( $header as $col ) {
        $col = preg_replace( '/^\xEF\xBB\xBF/', '', $col ); // strip BOM
        $normalized_header[] = strtolower( trim( $col ) );
    }

    // Expect exactly: post_id, related_post_id, similarity, rank
    $index_post_id         = array_search( 'post_id', $normalized_header, true );
    $index_related_post_id = array_search( 'related_post_id', $normalized_header, true );
    $index_similarity      = array_search( 'similarity', $normalized_header, true );
    $index_rank            = array_search( 'rank', $normalized_header, true );

    if ( $index_post_id === false || $index_related_post_id === false || $index_similarity === false || $index_rank === false ) {
        fclose( $handle );
        add_settings_error(
            'bf_re_emb_messages',
            'bf_re_emb_missing_columns',
            __( 'CSV must contain columns: post_id, related_post_id, similarity, rank.', 'bf-wp-related-embeddings-db' ),
            'error'
        );
        return;
    }

    $inserted   = 0;
    $first_data = null;

    while ( ( $row = fgetcsv( $handle ) ) !== false ) {
        // Skip completely empty lines.
        if ( empty( array_filter( $row, 'strlen' ) ) ) {
            continue;
        }

        $post_id         = isset( $row[ $index_post_id ] ) ? (int) $row[ $index_post_id ] : 0;
        $related_post_id = isset( $row[ $index_related_post_id ] ) ? (int) $row[ $index_related_post_id ] : 0;
        $similarity_raw  = isset( $row[ $index_similarity ] ) ? $row[ $index_similarity ] : '0';
        $rank            = isset( $row[ $index_rank ] ) ? (int) $row[ $index_rank ] : 0;

        // Use floatval in case of locale issues.
        $similarity = (float) str_replace( ',', '.', $similarity_raw );

        if ( $post_id <= 0 || $related_post_id <= 0 || $rank <= 0 ) {
            continue;
        }

        if ( $first_data === null ) {
            $first_data = array(
                'post_id'         => $post_id,
                'related_post_id' => $related_post_id,
                'similarity'      => $similarity,
                'rank'            => $rank,
            );
            error_log( '[bf_wp_related_embeddings_db] First CSV data row parsed: ' . wp_json_encode( $first_data ) );
        }

        $result = $wpdb->insert(
            $table_name,
            array(
                'post_id'         => $post_id,
                'related_post_id' => $related_post_id,
                'similarity'      => $similarity,
                'rank'            => $rank,
            ),
            array( '%d', '%d', '%f', '%d' )
        );

        if ( $result !== false ) {
            $inserted++;
        }
    }

    fclose( $handle );

    error_log( sprintf(
        '[bf_wp_related_embeddings_db] Import finished: %d rows inserted into %s',
        $inserted,
        $table_name
    ) );

    add_settings_error(
        'bf_re_emb_messages',
        'bf_re_emb_import_success',
        sprintf(
            __( 'Imported %d related rows (table truncated before import).', 'bf-wp-related-embeddings-db' ),
            $inserted
        ),
        'updated'
    );
}

/**
 * Settings page.
 */
function bf_re_emb_render_settings_page() {
    if ( isset( $_POST['bf_re_emb_import_submit'] ) ) {
        bf_re_emb_handle_csv_import();
    }

    settings_errors( 'bf_re_emb_messages' );

    ?>
    <div class="wrap">
        <h1><?php esc_html_e( 'Related Posts Embeddings Import', 'bf-wp-related-embeddings-db' ); ?></h1>

        <p>
            <?php esc_html_e(
                'Upload a CSV file with columns: post_id, related_post_id, similarity, rank. The plugin will TRUNCATE the custom table and load the new data.',
                'bf-wp-related-embeddings-db'
            ); ?>
        </p>

        <p>
            <?php
            printf(
                esc_html__( 'Typical file name from your pipeline: %s', 'bf-wp-related-embeddings-db' ),
                '<code>' . esc_html( BF_RE_EMB_DEFAULT_CSV_FILENAME ) . '</code>'
            );
            ?>
        </p>

        <form method="post" enctype="multipart/form-data">
            <?php wp_nonce_field( 'bf_re_emb_import_csv', 'bf_re_emb_import_nonce' ); ?>

            <table class="form-table" role="presentation">
                <tr>
                    <th scope="row">
                        <label for="bf_re_emb_csv"><?php esc_html_e( 'CSV File', 'bf-wp-related-embeddings-db' ); ?></label>
                    </th>
                    <td>
                        <input type="file" id="bf_re_emb_csv" name="bf_re_emb_csv" accept=".csv,text/csv" />
                    </td>
                </tr>
            </table>

            <?php submit_button(
                __( 'Import CSV (truncate & reload)', 'bf-wp-related-embeddings-db' ),
                'primary',
                'bf_re_emb_import_submit'
            ); ?>
        </form>
    </div>
    <?php
}
```

***

## What to do now

1. In WordPress:

   - Deactivate and delete the old plugin.  
   - Create folder `wp-content/plugins/bf_wp_related_embeddings_db/`.  
   - Save this file as `bf_wp_related_embeddings_db.php` inside.  
   - Activate the plugin.

2. In phpMyAdmin:

   - Confirm table `wp_related_posts_embeddings` exists.  
   - If not, check your PHP error log inside the Docker container for `dbDelta` errors.

3. Import CSV:

   - Go to Settings → Related Embeddings.  
   - Upload your CSV.  
   - Check `wp-content/debug.log` or container logs:
     - You should see “[bf_wp_related_embeddings_db] Uploaded CSV: ... size: xxx bytes”.  
     - And a “First CSV data row parsed” log with your first row (11463,13091,...).  

4. In phpMyAdmin:

   - Run: `SELECT COUNT(*) FROM wp_related_posts_embeddings;`  
   - You should see a non‑zero count.  
   - Run: `SELECT * FROM wp_related_posts_embeddings ORDER BY post_id, rank LIMIT 10;` to confirm the data.

Once this works, the meta box will show these relations on the post edit screen.



The plugin bf_test_table.php is working I see the table but when i unstall the plugin, the table is still there. Can you fix it.
