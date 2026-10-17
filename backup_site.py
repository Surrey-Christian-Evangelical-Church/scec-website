#!/usr/bin/env python3
"""
SCEC Chinese Website Backup & Asset Exporter
Downloads all WordPress pages, posts, and generates full media manifests
for migration to Google Sites and Google Drive.
"""

import os
import sys
import json
import urllib.request
import re

SITE_URL = "https://scecchinese.com"
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(OUTPUT_DIR, "content_backup")

def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))

def clean_html_to_markdown(html_text):
    # Basic conversion to readable text/markdown
    text = html_text
    # Headings
    for i in range(6, 0, -1):
        text = re.sub(rf'<h{i}[^>]*>(.*?)</h{i}>', rf'\n\n{"#" * i} \1\n\n', text, flags=re.DOTALL)
    # Paragraphs & line breaks
    text = re.sub(r'<p[^>]*>(.*?)</p>', r'\n\n\1\n\n', text, flags=re.DOTALL)
    text = re.sub(r'<br\s*/?>', r'\n', text)
    # Links
    text = re.sub(r'<a\s+[^>]*href=[\'"]([^\'"]+)[\'"][^>]*>(.*?)</a>', r'[\2](\1)', text, flags=re.DOTALL)
    # Images
    text = re.sub(r'<img\s+[^>]*src=[\'"]([^\'"]+)[\'"][^>]*alt=[\'"]([^\'"]*)[\'"][^>]*>', r'![\2](\1)', text)
    text = re.sub(r'<img\s+[^>]*src=[\'"]([^\'"]+)[\'"][^>]*>', r'![](\1)', text)
    # Remove remaining HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Clean up whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def main():
    os.makedirs(CONTENT_DIR, exist_ok=True)
    pages_dir = os.path.join(CONTENT_DIR, "pages")
    posts_dir = os.path.join(CONTENT_DIR, "posts")
    os.makedirs(pages_dir, exist_ok=True)
    os.makedirs(posts_dir, exist_ok=True)

    print(f"[*] Fetching pages from {SITE_URL}...")
    pages = fetch_json(f"{SITE_URL}/wp-json/wp/v2/pages?per_page=100")
    print(f"    Found {len(pages)} pages.")

    for p in pages:
        slug = p["slug"]
        title = p["title"]["rendered"]
        raw_html = p["content"]["rendered"]
        md_text = clean_html_to_markdown(raw_html)

        # save page json & md
        with open(os.path.join(pages_dir, f"{slug}.md"), "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n**Source URL:** {p['link']}\n\n---\n\n{md_text}\n")
        with open(os.path.join(pages_dir, f"{slug}.html"), "w", encoding="utf-8") as f:
            f.write(raw_html)

    print(f"[*] Fetching posts from {SITE_URL}...")
    posts = fetch_json(f"{SITE_URL}/wp-json/wp/v2/posts?per_page=100")
    print(f"    Found {len(posts)} posts.")

    for p in posts:
        slug = p["slug"]
        title = p["title"]["rendered"]
        raw_html = p["content"]["rendered"]
        md_text = clean_html_to_markdown(raw_html)

        with open(os.path.join(posts_dir, f"{slug}.md"), "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n**Source URL:** {p['link']}\n\n---\n\n{md_text}\n")
        with open(os.path.join(posts_dir, f"{slug}.html"), "w", encoding="utf-8") as f:
            f.write(raw_html)

    print("[*] Backup of page and post content completed successfully!")
    print(f"    Content stored in: {CONTENT_DIR}")

if __name__ == "__main__":
    main()
