<?php

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

class WebMCP_Admin {

    public static function register_menu() {
        add_options_page(
            'WebMCP Settings',
            'WebMCP',
            'manage_options',
            'webmcp-settings',
            [ __CLASS__, 'render_page' ]
        );
    }

    public static function register_settings() {
        register_setting( 'webmcp_group', 'webmcp_enabled', [ 'sanitize_callback' => 'absint' ] );
        register_setting( 'webmcp_group', 'webmcp_tools',   [ 'sanitize_callback' => [ __CLASS__, 'sanitize_tools' ] ] );
    }

    public static function sanitize_tools( $input ) {
        $valid = [ 'search_posts', 'list_categories', 'get_latest', 'get_toc', 'get_related' ];
        $out   = [];
        foreach ( $valid as $key ) {
            $out[ $key ] = ! empty( $input[ $key ] ) ? 1 : 0;
        }
        return $out;
    }

    public static function render_page() {
        if ( ! current_user_can( 'manage_options' ) ) {
            return;
        }

        $tools        = get_option( 'webmcp_tools', [] );
        $enabled      = get_option( 'webmcp_enabled', 1 );
        $manifest_url = rest_url( 'webmcp/v1/manifest' );
        $rest_base    = rest_url( 'webmcp/v1' );
        $site_url     = get_site_url();

        $active_tab = isset( $_GET['tab'] ) ? sanitize_key( $_GET['tab'] ) : 'settings';
        $page_url   = admin_url( 'options-general.php?page=webmcp-settings' );
        ?>
        <div class="wrap">
            <h1>WebMCP <span style="font-size:13px;color:#666;font-weight:normal;">v<?php echo esc_html( WEBMCP_VERSION ); ?></span></h1>
            <p style="color:#555;">Exposes WordPress content as structured tools for AI agents — <a href="https://webmcp.dev" target="_blank" rel="noopener">WebMCP proposed standard</a>.</p>

            <nav class="nav-tab-wrapper">
                <a href="<?php echo esc_url( $page_url . '&tab=settings' ); ?>"
                   class="nav-tab <?php echo $active_tab === 'settings' ? 'nav-tab-active' : ''; ?>">Settings</a>
                <a href="<?php echo esc_url( $page_url . '&tab=manifest' ); ?>"
                   class="nav-tab <?php echo $active_tab === 'manifest' ? 'nav-tab-active' : ''; ?>">Manifest</a>
                <a href="<?php echo esc_url( $page_url . '&tab=help' ); ?>"
                   class="nav-tab <?php echo $active_tab === 'help' ? 'nav-tab-active' : ''; ?>">Help &amp; Verify</a>
            </nav>

            <?php if ( $active_tab === 'settings' ) : ?>

                <form method="post" action="options.php" style="margin-top:16px;">
                    <?php settings_fields( 'webmcp_group' ); ?>
                    <table class="form-table" role="presentation">
                        <tr>
                            <th scope="row">Plugin enabled</th>
                            <td>
                                <input type="checkbox" name="webmcp_enabled" value="1" <?php checked( $enabled, 1 ); ?>>
                                <span class="description">Injects MCP manifest in <code>&lt;head&gt;</code> and activates REST endpoints.</span>
                            </td>
                        </tr>
                        <tr>
                            <th scope="row">Enabled tools</th>
                            <td>
                                <?php
                                $tool_labels = [
                                    'search_posts'    => 'search_posts — search posts by keyword',
                                    'list_categories' => 'list_categories — list all categories',
                                    'get_latest'      => 'get_latest_posts — latest posts by category',
                                    'get_toc'         => 'get_post_toc — extract headings from a post',
                                    'get_related'     => 'get_related_posts — posts in same categories',
                                ];
                                foreach ( $tool_labels as $key => $label ) : ?>
                                    <label style="display:block;margin-bottom:6px;">
                                        <input type="checkbox"
                                               name="webmcp_tools[<?php echo esc_attr( $key ); ?>]"
                                               value="1"
                                            <?php checked( ! empty( $tools[ $key ] ) ); ?>>
                                        <code><?php echo esc_html( $label ); ?></code>
                                    </label>
                                <?php endforeach; ?>
                            </td>
                        </tr>
                    </table>
                    <?php submit_button(); ?>
                </form>

            <?php elseif ( $active_tab === 'manifest' ) : ?>

                <div style="margin-top:16px;">
                    <h2 style="margin-top:0;">Live Manifest</h2>
                    <p>URL: <a href="<?php echo esc_url( $manifest_url ); ?>" target="_blank"><?php echo esc_html( $manifest_url ); ?></a></p>
                    <pre style="background:#f6f7f7;padding:12px;overflow:auto;max-height:500px;border:1px solid #ddd;"><?php
                        $manifest = WebMCP_Manifest::build();
                        echo esc_html( wp_json_encode( $manifest, JSON_PRETTY_PRINT ) );
                    ?></pre>
                </div>

            <?php elseif ( $active_tab === 'help' ) : ?>

                <div style="margin-top:16px;max-width:860px;">

                    <h2 style="margin-top:0;">What Is WebMCP</h2>
                    <p>
                        WebMCP is a <strong>proposed web standard</strong> (not yet W3C — status 2026) that annotates HTML pages
                        so AI agents can discover and call structured tools without guessing from page layout.
                        It works like an OpenAPI spec, but for browser interactions instead of REST APIs.
                    </p>
                    <p>
                        This plugin injects a <code>&lt;script type="application/mcp+json"&gt;</code> manifest in every page
                        <code>&lt;head&gt;</code> and exposes REST endpoints that agents (Perplexity, Claude, ChatGPT Browse)
                        can call directly to search, browse, and discover content on your blog.
                    </p>
                    <p>
                        <strong>Spec status:</strong> proposed, not finalized.
                        <a href="https://webmcp.dev" target="_blank" rel="noopener">webmcp.dev</a>
                    </p>

                    <hr>
                    <h2>How Agents Discover This Plugin</h2>
                    <ol>
                        <li><strong>Manifest in <code>&lt;head&gt;</code></strong> — every page contains a <code>&lt;script type="application/mcp+json"&gt;</code> block with the full tool list. A browser-based AI agent reads this to know what tools are available before doing anything.</li>
                        <li><strong><code>&lt;link rel="mcp-manifest"&gt;</code></strong> — a second tag in <code>&lt;head&gt;</code> points to the manifest REST URL so agents can fetch it independently.</li>
                        <li><strong><code>data-mcp-*</code> attributes</strong> — key DOM elements (search form, category links) carry annotations so browser agents can locate entry points without parsing the manifest first.</li>
                        <li><strong>REST endpoints</strong> — agents call these directly to execute tools (search, browse categories, get TOC, etc.).</li>
                    </ol>
                    <p><strong>The manifest is identical on every page</strong> — it describes site-wide tools, not page-specific content. A single post page and a category archive page both receive the same manifest.</p>

                    <hr>
                    <h2>Pages That Receive the Manifest</h2>
                    <ul>
                        <li>Single post pages</li>
                        <li>Category archive pages</li>
                        <li>Tag archive pages</li>
                        <li>Home / blog index</li>
                        <li>Static pages</li>
                        <li>Search results</li>
                    </ul>
                    <p><strong>Condition:</strong> the active theme must call <code>wp_head()</code> — all standard WordPress themes do. If manifest is missing, that is the first thing to check.</p>

                    <hr>
                    <h2>How to Verify — 4 Methods</h2>

                    <h3>Method 1 — View Source (quickest)</h3>
                    <p>Open any page in your browser, press <kbd>Ctrl+U</kbd> (Windows/Linux) or <kbd>Cmd+U</kbd> (Mac), then search for <code>mcp</code>.</p>
                    <p>You should see two lines near the top of <code>&lt;head&gt;</code>:</p>
                    <pre style="background:#f6f7f7;padding:10px;border:1px solid #ddd;overflow:auto;">&lt;script type="application/mcp+json"&gt;{"schema_version":"0.1","name":...}&lt;/script&gt;
&lt;link rel="mcp-manifest" href="<?php echo esc_html( $manifest_url ); ?>"&gt;</pre>

                    <h3>Method 2 — curl (multi-page check)</h3>
                    <p>Run these in a terminal. Each should return 2 lines containing <code>mcp</code>:</p>
                    <pre style="background:#f6f7f7;padding:10px;border:1px solid #ddd;overflow:auto;"># Any post page
curl -s "<?php echo esc_html( $site_url ); ?>/your-post-slug/" | grep -i "mcp"

# Category archive
curl -s "<?php echo esc_html( $site_url ); ?>/category/your-category/" | grep -i "mcp"

# Tag archive
curl -s "<?php echo esc_html( $site_url ); ?>/tag/your-tag/" | grep -i "mcp"

# Home page
curl -s "<?php echo esc_html( $site_url ); ?>/" | grep -i "mcp"</pre>

                    <h3>Method 3 — Manifest endpoint (validates tool definitions)</h3>
                    <p>Open this URL in your browser — returns full JSON with all enabled tools:</p>
                    <pre style="background:#f6f7f7;padding:10px;border:1px solid #ddd;overflow:auto;"><a href="<?php echo esc_url( $manifest_url ); ?>" target="_blank"><?php echo esc_html( $manifest_url ); ?></a></pre>
                    <p>Expect: <code>tools</code> array with up to 5 entries. If array is empty, all tools are disabled in Settings.</p>

                    <h3>Method 4 — REST endpoints (validates each tool works)</h3>
                    <p>Open each URL in your browser (or curl). Expect JSON arrays:</p>
                    <table class="widefat striped" style="margin-bottom:8px;">
                        <thead><tr><th>Tool</th><th>Test URL</th></tr></thead>
                        <tbody>
                            <tr>
                                <td><code>list_categories</code></td>
                                <td><a href="<?php echo esc_url( $rest_base . '/categories' ); ?>" target="_blank"><?php echo esc_html( $rest_base . '/categories' ); ?></a></td>
                            </tr>
                            <tr>
                                <td><code>get_latest_posts</code></td>
                                <td><a href="<?php echo esc_url( $rest_base . '/posts?count=5' ); ?>" target="_blank"><?php echo esc_html( $rest_base . '/posts?count=5' ); ?></a></td>
                            </tr>
                            <tr>
                                <td><code>search_posts</code></td>
                                <td><a href="<?php echo esc_url( $rest_base . '/search?query=wordpress' ); ?>" target="_blank"><?php echo esc_html( $rest_base . '/search?query=wordpress' ); ?></a></td>
                            </tr>
                            <tr>
                                <td><code>get_post_toc</code></td>
                                <td><code><?php echo esc_html( $rest_base ); ?>/post/{id}/toc</code> — replace <code>{id}</code> with a post ID from the list above</td>
                            </tr>
                            <tr>
                                <td><code>get_related_posts</code></td>
                                <td><code><?php echo esc_html( $rest_base ); ?>/post/{id}/related</code> — same, replace <code>{id}</code></td>
                            </tr>
                        </tbody>
                    </table>

                    <hr>
                    <h2>Tool Reference</h2>
                    <table class="widefat striped">
                        <thead>
                            <tr><th>Tool</th><th>Endpoint</th><th>Parameters</th><th>Returns</th></tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code>search_posts</code></td>
                                <td><code>GET /search</code></td>
                                <td><code>query</code> (req), <code>category</code>, <code>limit</code> (max 20)</td>
                                <td>Array of matching posts</td>
                            </tr>
                            <tr>
                                <td><code>get_latest_posts</code></td>
                                <td><code>GET /posts</code></td>
                                <td><code>category</code>, <code>count</code> (max 20)</td>
                                <td>Most recent posts</td>
                            </tr>
                            <tr>
                                <td><code>list_categories</code></td>
                                <td><code>GET /categories</code></td>
                                <td>none</td>
                                <td>All non-empty categories with counts + URLs</td>
                            </tr>
                            <tr>
                                <td><code>get_post_toc</code></td>
                                <td><code>GET /post/{id}/toc</code></td>
                                <td><code>id</code> (req)</td>
                                <td>H2–H4 headings array</td>
                            </tr>
                            <tr>
                                <td><code>get_related_posts</code></td>
                                <td><code>GET /post/{id}/related</code></td>
                                <td><code>id</code> (req), <code>limit</code> (max 10)</td>
                                <td>Posts sharing same categories</td>
                            </tr>
                        </tbody>
                    </table>

                    <hr>
                    <h2>What This Plugin Does NOT Do</h2>
                    <ul>
                        <li><strong>No direct Google ranking benefit</strong> — AI citation ≠ ranking signal (as of 2026).</li>
                        <li><strong>No automatic Perplexity / ChatGPT integration</strong> — agents must implement WebMCP client-side to use the manifest. Adoption is still growing.</li>
                        <li><strong>No page-specific annotations</strong> — manifest is site-wide, not per-post. Content-level structured data (Schema.org Article) is a separate concern.</li>
                        <li><strong>No guaranteed spec stability</strong> — WebMCP is proposed, not finalized. This plugin targets schema_version 0.1.</li>
                        <li><strong>No user interaction tools</strong> — plugin is read-only. No comment forms, no checkout, no newsletter subscription exposed (none active on site).</li>
                    </ul>

                    <hr>
                    <h2>Troubleshooting</h2>
                    <table class="widefat striped">
                        <thead><tr><th>Symptom</th><th>Cause</th><th>Fix</th></tr></thead>
                        <tbody>
                            <tr>
                                <td>No <code>mcp</code> in page source</td>
                                <td>Theme does not call <code>wp_head()</code>, or plugin disabled</td>
                                <td>Check Settings tab — plugin enabled? Check theme's <code>header.php</code> for <code>&lt;?php wp_head(); ?&gt;</code></td>
                            </tr>
                            <tr>
                                <td>REST endpoints return 404</td>
                                <td>Pretty permalinks not enabled</td>
                                <td>Settings → Permalinks → select any option except Plain → Save</td>
                            </tr>
                            <tr>
                                <td><code>tools</code> array is empty in manifest</td>
                                <td>All tools unchecked in Settings</td>
                                <td>Settings tab → enable at least one tool → Save</td>
                            </tr>
                            <tr>
                                <td><code>get_post_toc</code> returns empty <code>toc</code> array</td>
                                <td>Post content uses blocks without heading tags, or headings are H1/H5+</td>
                                <td>Plugin parses H2–H4 only. Check post HTML source for heading tags.</td>
                            </tr>
                            <tr>
                                <td>WP notice about <code>register_rest_route</code> on wrong action</td>
                                <td>Old plugin version (pre 1.0.1) used <code>init</code> hook</td>
                                <td>Update to v1.0.1+ — routes now correctly registered on <code>rest_api_init</code></td>
                            </tr>
                        </tbody>
                    </table>

                </div>

            <?php endif; ?>
        </div>
        <?php
    }
}
