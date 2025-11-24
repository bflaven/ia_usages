#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
conda create --name generate_llm_txt python=3.9.13
conda info --envs
source activate generate_llm_txt
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n generate_llm_txt


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

pip install beautifulsoup4
pip install requests

python -m pip install beautifulsoup4
python -m pip install requests

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/_ia_semantic_layer/generate_sitemap_xml/

# LAUNCH the file
python 001_generate_sitemap_xml.py

"""
import requests
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, ElementTree

# ======= CONFIGURATION ========
BASE_URL = "[your-wordpress-site]"
API_BASE = f"{BASE_URL}/wp-json/wp/v2"
MAX_POSTS = 657
MAX_PAGES = 15
MAX_CATEGORIES = 103
MAX_TAGS = 2475

PER_PAGE = 20   # API limit (default 10, WordPress max 100)

ENDPOINTS = [
    # Classic
    ("posts", MAX_POSTS, "post"),
    ("pages", MAX_PAGES, "page"),
    ("categories", MAX_CATEGORIES, "category"),
    ("tags", MAX_TAGS, "tag"),
    # Custom post types
    ("bf_videos_manager", 106, "bf_videos_manager"),
    ("bf_quotes_manager", 65, "bf_quotes_manager"),
    ("clients", 63, "clients"),
    ("product_for_sale", 47, "product_for_sale"),
    # Custom taxonomies
    ("bf_videos_manager_tag", 170, "bf_videos_manager_tag"),
    ("bf_videos_manager_cat", 17, "bf_videos_manager_cat"),
    ("bf_quotes_manager_author", 53, "bf_quotes_manager_author"),
    ("bf_quotes_manager_flavor", 261, "bf_quotes_manager_flavor"),
    ("product_for_sale_kw", 32, "product_for_sale_kw"),
    ("product_for_sale_author", 68, "product_for_sale_author"),
]

# endpoints for which date/orderby/order is allowed
ORDERABLE_ENDPOINTS = {'posts', 'pages', 'bf_videos_manager', 'bf_quotes_manager', 'clients', 'product_for_sale'}

def get_paginated(endpoint, max_items):
    """Safely fetch every item from paginated REST endpoint."""
    url = f"{API_BASE}/{endpoint}"
    page = 1
    count = 0
    results = []
    while count < max_items:
        # Use ordering only for endpoints that support it!
        params = {'per_page': PER_PAGE, 'page': page}
        if endpoint in ORDERABLE_ENDPOINTS:
            params.update({'orderby': 'date', 'order': 'desc'})
        resp = requests.get(url, params=params)
        try:
            resp.raise_for_status()
        except requests.HTTPError as e:
            print(f"Error: {e}")
            break
        items = resp.json()
        if not items:
            break
        for item in items:
            results.append(item)
            count += 1
            if count >= max_items:
                break
        if len(items) < PER_PAGE:
            break
        page += 1
    return results

def wordpress_entry_to_url(item, content_type):
    """Return canonical URL and lastmod for any WP item."""
    link = item.get("link")
    lastmod = item.get("modified_gmt") or item.get("date_gmt")
    if link is None and "slug" in item:
        link = f"{BASE_URL}/{content_type}/{item['slug']}/"
    if not link:
        return None, None
    if lastmod:
        if not lastmod.endswith("+00:00"):
            lastmod += "+00:00"
    else:
        lastmod = datetime.utcnow().isoformat() + "+00:00"
    return link, lastmod

def create_xml_urlset(url_entries):
    urlset = Element('urlset')
    urlset.set('xmlns', "http://www.sitemaps.org/schemas/sitemap/0.9")
    for url, lastmod, priority in url_entries:
        url_elem = SubElement(urlset, 'url')
        SubElement(url_elem, 'loc').text = url
        SubElement(url_elem, 'lastmod').text = lastmod
        SubElement(url_elem, 'priority').text = f"{priority:.2f}"
    return urlset

if __name__ == "__main__":
    url_entries = []
    for endpoint, max_items, label in ENDPOINTS:
        print(f"Fetching {label} from endpoint: {endpoint}")
        items = get_paginated(endpoint, max_items)
        for item in items:
            url, lastmod = wordpress_entry_to_url(item, label)
            if url:
                priority = 0.90 if label in {"home", "post", "page"} else 0.60
                url_entries.append((url, lastmod, priority))
    url_entries.append((f"{BASE_URL}/", datetime.utcnow().isoformat() + "+00:00", 0.90))
    urlset = create_xml_urlset(url_entries)
    ElementTree(urlset).write("sitemap.xml", encoding="utf-8", xml_declaration=True)
    print("Sitemap generated: sitemap.xml")


