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
cd cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_semantic_layer/generate_llm_txt


# LAUNCH the file
python 002_generate_llm_txt.py

"""
import requests
import time
from html import unescape
from bs4 import BeautifulSoup

API_URL = "[your-wordpress-site]/wp-json/wp/v2/posts"
# Your site wordpress stats
PER_PAGE = 20
# TOTAL_POSTS = 890
TOTAL_POSTS = 123
SUMMARY_CHARS = 150  # Number of chars to show before ...Continue reading
OUTPUT_FILE = "README_posts_2.md"



def get_posts(api_url, per_page, total_posts):
    posts = []
    pages = (total_posts // per_page) + int(total_posts % per_page > 0)
    for page in range(1, pages + 1):
        params = {
            "per_page": per_page,
            "page": page,
        }
        resp = requests.get(api_url, params=params)
        if resp.status_code != 200:
            print(f"Failed at page {page}: {resp.status_code}, retrying...")
            time.sleep(2)
            continue
        page_posts = resp.json()
        if not page_posts:
            break
        posts.extend(page_posts)
        print(f"Fetched page {page} ({len(page_posts)} posts)")
        time.sleep(0.2)  # polite delay
    return posts

def process_post(post):
    title = unescape(post["title"]["rendered"].strip())
    link = post["link"]
    # Remove HTML tags and get a plain-text preview
    raw_content = post["content"]["rendered"]
    soup = BeautifulSoup(raw_content, "html.parser")
    text_content = soup.get_text().replace('\n', ' ').strip()
    preview = text_content[:SUMMARY_CHARS].rstrip()
    out_line = f"- [{title}]({link}): {preview} ...Continue reading → {title}"
    return out_line

def main():
    posts = get_posts(API_URL, PER_PAGE, TOTAL_POSTS)
    lines = []
    for post in posts:
        try:
            line = process_post(post)
            lines.append(line)
        except Exception as e:
            print(f"Error processing post {post.get('id', '?')}: {e}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + '\n')
    print(f"Done! Wrote {len(lines)} posts to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

