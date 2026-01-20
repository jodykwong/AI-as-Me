"""Web search tool for Agent."""

import urllib.request
import urllib.parse
from typing import List, Dict


def search_web(query: str, num_results: int = 5) -> List[Dict]:
    """Search web using DuckDuckGo (no API key needed).

    Args:
        query: Search query
        num_results: Max results to return

    Returns:
        List of {title, url, snippet} dicts
    """
    encoded = urllib.parse.quote(query)
    url = f"https://html.duckduckgo.com/html/?q={encoded}"

    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8")
    except Exception as e:
        return [{"error": str(e)}]

    # Parse results (minimal regex parsing)
    import re

    results = []

    # Find result blocks
    pattern = r'<a rel="nofollow" class="result__a" href="([^"]+)"[^>]*>(.+?)</a>'
    matches = re.findall(pattern, html)

    for href, title in matches[:num_results]:
        # Clean title
        title = re.sub(r"<[^>]+>", "", title).strip()
        results.append({"title": title, "url": href, "snippet": ""})

    return results


def fetch_url(url: str, timeout: int = 15) -> str:
    """Fetch URL content as text.

    Args:
        url: URL to fetch
        timeout: Request timeout

    Returns:
        Page text content (stripped of HTML)
    """
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return f"Error: {e}"

    # Strip HTML tags
    import re

    text = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text[:8000]  # Limit length


if __name__ == "__main__":
    # Test
    results = search_web("RDK X5 ORB-SLAM3")
    for r in results:
        print(f"- {r['title']}: {r['url']}")
