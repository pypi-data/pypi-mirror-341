import time
from fastapi import HTTPException
from .utils import fetch_content, clean_html, get_internal_links

def crawl_depth_2(request) -> dict:
    base_url = str(request.url)
    visited = set()
    results = {}

    html1 = fetch_content(base_url)
    if not html1:
        raise HTTPException(status_code=400, detail="Failed to fetch base URL")

    results[base_url] = clean_html(html1) if request.clean_text else html1
    visited.add(base_url)

    internal_links = get_internal_links(base_url, html1)
    for link in list(internal_links)[:10]:
        if link not in visited:
            time.sleep(1)
            html2 = fetch_content(link)
            visited.add(link)
            if html2:
                results[link] = clean_html(html2) if request.clean_text else html2

    return results
