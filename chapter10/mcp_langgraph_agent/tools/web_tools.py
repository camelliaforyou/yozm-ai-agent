"""웹 관련 도구 (네이버 뉴스 대응 버전)"""
import httpx
from bs4 import BeautifulSoup

def scrape_page_text(url: str) -> str:
    """웹페이지의 텍스트 콘텐츠를 스크랩합니다."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        ),
        "Referer": "https://www.google.com/",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    # 리다이렉트 허용
    resp = httpx.get(url, headers=headers, follow_redirects=True, timeout=10)
    if resp.status_code != 200:
        return f"Failed to fetch {url} (status={resp.status_code})"

    soup = BeautifulSoup(resp.text, "html.parser")
    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
    text = " ".join(paragraphs)
    cleaned = " ".join(text.split())
    return cleaned[:8000] if cleaned else ""
