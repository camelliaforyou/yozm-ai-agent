"""뉴스 관련 도구"""
import feedparser


def get_news_headlines() -> str:
    """구글 RSS피드에서 최신 뉴스와 URL을 반환합니다."""
    rss_url = "https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(rss_url)

    if not feed.entries:
        return "뉴스를 가져올 수 없습니다."

    news_list = []
    for i, entry in enumerate(feed.entries, 1):
        # feedparser entry 객체에서 직접 속성 접근
        title = getattr(entry, "title", "제목 없음")
        link = getattr(entry, "link", "#")

        # 디버깅을 위한 로그 추가
        print(f"뉴스 {i}: {title} - {link}")

        # None 값이나 빈 문자열 처리
        if not title or title == "None":
            title = "제목 없음"
        if not link or link == "None":
            link = "#"

        # 마크다운 링크 형식으로 포맷팅
        news_item = f"{i}. [{title}]({link})"
        news_list.append(news_item)

    # 번호가 매겨진 리스트를 문자열로 반환
    return "\n".join(news_list)

