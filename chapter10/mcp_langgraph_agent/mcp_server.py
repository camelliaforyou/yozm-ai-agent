"""MCP 서버 - 도구들을 로드하고 서버를 실행"""
from mcp.server.fastmcp import FastMCP
from tools import web_tools, weather_tools, news_tools, sports_tools, schedule_tools, llm_tools, finance_tools
import dotenv

dotenv.load_dotenv()

# MCP 서버 인스턴스 생성
mcp = FastMCP("Yozm-ai-agent")

# 도구들을 MCP 서버에 등록
@mcp.tool()
def summarize_webpage(url: str) -> str:
    """주어진 웹페이지를 요약합니다."""
    return llm_tools.summarize_webpage(url)


@mcp.tool()
def get_exchange_rate(base: str = "USD", target: str = "KRW") -> str:
    """기준 통화 대비 환율을 조회합니다."""
    return finance_tools.get_exchange_rate(base, target)

@mcp.tool()
def get_weather(city_name: str) -> str:
    """도시 이름을 받아 해당 도시의 현재 날씨 정보를 반환합니다."""
    return weather_tools.get_weather(city_name)


@mcp.tool()
def get_news_headlines() -> str:
    """구글 RSS피드에서 최신 뉴스와 URL을 반환합니다."""
    return news_tools.get_news_headlines()


@mcp.tool()
def get_kbo_rank() -> str:
    """한국 프로야구 구단의 랭킹을 가져옵니다"""
    return sports_tools.get_kbo_rank()


@mcp.tool()
def today_schedule() -> str:
    """임의의 스케줄을 반환합니다."""
    return schedule_tools.today_schedule()


@mcp.tool()
def daily_quote() -> str:
    """사용자에게 영감을 주는 명언을 출력합니다"""
    return llm_tools.daily_quote()


@mcp.tool()
def brief_today() -> str:
    """사용자의 하루 시작을 돕기 위해 날씨, 뉴스, 일정 등을 종합하여 전달합니다."""
    return llm_tools.brief_today()


# ⑨ 메인 실행 부분
if __name__ == "__main__":
    # MCP 서버 실행 (HTTP 스트리밍 모드, 포트 8000)
    mcp.run(transport="streamable-http")
