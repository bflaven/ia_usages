/**
 * WebMCP client helper
 * Annotates key DOM elements with data-mcp-* attributes so browser-based
 * AI agents can locate interactive entry points without parsing the manifest.
 */
(function () {
  'use strict';

  if (typeof webmcpConfig === 'undefined') return;

  const base = webmcpConfig.restUrl;

  // Annotate the WP search form if present
  const searchForm = document.querySelector('.search-form, form[role="search"]');
  if (searchForm) {
    searchForm.setAttribute('data-mcp-tool', 'search_posts');
    searchForm.setAttribute('data-mcp-action', base + 'search');
    searchForm.setAttribute('data-mcp-method', 'GET');

    const searchInput = searchForm.querySelector('input[type="search"], input[name="s"]');
    if (searchInput) {
      searchInput.setAttribute('data-mcp-param', 'query');
      searchInput.setAttribute('data-mcp-required', 'true');
    }
  }

  // Annotate category links
  document.querySelectorAll('a[href*="/category/"]').forEach(function (link) {
    const slug = link.href.replace(/.*\/category\/([^/]+)\/?$/, '$1');
    link.setAttribute('data-mcp-tool', 'get_latest_posts');
    link.setAttribute('data-mcp-param-category', slug);
  });

  // Expose manifest URL as a meta-discoverable attribute on <body>
  document.body.setAttribute('data-mcp-manifest', base + '../manifest');
  document.body.setAttribute('data-mcp-site', webmcpConfig.siteName);
})();
