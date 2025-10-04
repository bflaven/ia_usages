#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
conda create --name geo_llms_txt_poc python=3.9.13
conda info --envs
source activate geo_llms_txt_poc
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n geo_llms_txt_poc


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
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_using_n8n_io/generative_engine_optimization_llms_txt


# LAUNCH the file
python 003_generative_engine_optimization_llms_txt.py

"""


import requests
from bs4 import BeautifulSoup

BASE_URL = "https://flaven.fr"
N_POSTS = 20
N_PAGES = 4  # This usually covers 20 posts (5 per page)
GITHUB_URL = "https://github.com/bflaven?tab=repositories"
N_REPOS = 10

def get_soup(url):
    resp = requests.get(url, timeout=10)
    if resp.status_code == 200:
        return BeautifulSoup(resp.text, "html.parser")
    return None

def extract_posts(soups, n_posts=N_POSTS):
    posts = []
    for soup in soups:
        post_wrapper = soup.find('div', class_='post-wrapper-hentry')
        if not post_wrapper:
            continue
        for article in post_wrapper.find_all('article'):
            h1 = article.find('h1', class_='entry-title')
            content_div = article.find('div', class_='entry-summary')
            if h1 and content_div and h1.find('a'):
                title = h1.get_text(strip=True)
                link = h1.find('a')['href']
                summary = content_div.get_text(strip=True)
                posts.append((title, link, summary))
                if len(posts) >= n_posts:
                    return posts
    return posts

def extract_pages(soup, n_pages=10):
    pages = []
    nav = soup.find("nav")
    if nav:
        for a in nav.find_all("a", href=True):
            href = a['href']
            if '/page/' not in href and BASE_URL in href:
                text = a.get_text(strip=True)
                pages.append((text, href))
    seen = set()
    unique = []
    for t, h in pages:
        if h not in seen:
            unique.append((t, h))
            seen.add(h)
        if len(unique) >= n_pages:
            break
    return unique

def extract_github_repos(url, n_repos=N_REPOS):
    soup = get_soup(url)
    repos = []
    if soup:
        repo_items = soup.find_all('li', class_='public')
        # If li.public fails due to github html, fallback to direct repo blocks
        count = 0
        for h3 in soup.find_all('h3', class_='wb-break-all'):
            repo_link = h3.find('a')
            if not repo_link:
                continue
            repo_name = repo_link.text.strip()
            repo_url = 'https://github.com' + repo_link['href']
            desc_tag = None
            # Description is not inside h3, it's after, so search the li container
            parent_li = h3.find_parent('li')
            if parent_li:
                desc_tag = parent_li.find(attrs={"itemprop": "description"})
            desc = desc_tag.get_text(strip=True) if desc_tag else ""
            repos.append((repo_name, repo_url, desc))
            count += 1
            if count >= n_repos:
                break
    return repos

def scrape_main():
    soups = []
    for i in range(1, N_PAGES + 1):
        page_url = BASE_URL if i == 1 else f"{BASE_URL}/page/{i}/"
        soup = get_soup(page_url)
        if soup:
            soups.append(soup)
        else:
            break

    posts = extract_posts(soups, N_POSTS)
    main_soup = soups[0] if soups else None
    pages = extract_pages(main_soup) if main_soup else []
    code_repos = extract_github_repos(GITHUB_URL, N_REPOS)

    llms_txt = [
        "# Bruno Flaven's website",
        "",
        "> Professional blog of Bruno Flaven, currently working as AI Coordinator with over 20 years' experience. More at [flaven.fr](https://flaven.fr) or [LinkedIn](https://www.linkedin.com/in/brunoflaven).",
        "",
        "## Homepage",
        f"- [Homepage]({BASE_URL}): Bruno Flaven's personal and professional articles on AI, mobile, and digital product management.",
        "",
        "## Posts"
    ]
    for title, link, desc in posts:
        llms_txt.append(f"- [{title}]({link}): {desc}")
    llms_txt.append("")
    llms_txt.append("## Pages")
    for title, link in pages:
        llms_txt.append(f"- [{title}]({link})")
    llms_txt.append("")
    llms_txt.append("## Code")
    for repo_name, repo_url, repo_desc in code_repos:
        if repo_desc:
            llms_txt.append(f"- [{repo_name}]({repo_url}): {repo_desc}")
        else:
            llms_txt.append(f"- [{repo_name}]({repo_url})")
    llms_txt.append("")
    llms_txt.append("## Optional")
    llms_txt.append(f"- [LinkedIn profile](https://www.linkedin.com/in/brunoflaven)")
    llms_txt.append(f"- [Youtube](https://www.youtube.com/channel/UCnUBoVx9Yai3wirPBvNpNQw)")
    llms_txt.append(f"- [Github](https://github.com/bflaven/)")
    llms_txt.append(f"- [Amazon](https://amzn.to/2WQbRpA)")
    llms_txt.append(f"[comment]: # (Generated by Bruno for flaven.fr)")


    with open("llms_model_extended_flaven_fr.txt", "w", encoding="utf-8") as f:
        f.write('\n'.join(llms_txt))
    print("llms_model_extended_flaven_fr.txt file successfully created!")
    print("CAUTION: rename llms_model_extended_flaven_fr.txt file in llms.txt before upload ")

if __name__ == "__main__":
    scrape_main()



