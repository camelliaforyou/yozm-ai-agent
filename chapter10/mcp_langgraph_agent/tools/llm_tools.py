"""LLM을 활용한 도구"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from . import web_tools


def summarize_webpage(url: str) -> str:
    """웹페이지 내용을 분석하고 요약합니다."""
    try:
        text = web_tools.scrape_page_text(url)
        if not text or len(text.strip()) < 200:
            return f"본문이 짧지만 시도해보겠습니다:\n\n{text[:500]}"

        # LLM 모델 초기화
        chat_model = ChatOpenAI(model="gpt-4o-mini")

        # 프롬프트 생성
        prompt = ChatPromptTemplate.from_messages([
            ("system", "당신은 신뢰성 있는 기사 요약 도우미입니다."),
            ("human", f"다음 웹페이지의 내용을 5줄 이내로 핵심만 요약해주세요:\n\n{text[:4000]}")
        ])

        chain = prompt | chat_model
        response = chain.invoke({})
        return f"## 요약 결과\n\n{response.content.strip()}"
    except Exception as e:
        return f"웹페이지 요약 중 오류 발생: {e}"

def daily_quote() -> str:
    """사용자에게 영감을 주는 명언을 출력합니다"""
    chat_model = ChatOpenAI(model="gpt-4o-mini")
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "당신은 오늘 하루의 명언을 알려주는 도우미입니다. 사용자의 명언 요청이 있을시 명언만 출력합니다.",
            ),
            ("human", "오늘의 명언을 출력해주세요. "),
        ]
    )
    chain = prompt | chat_model
    response = chain.invoke({})
    return response.content


def brief_today() -> str:
    """사용자의 하루 시작을 돕기 위해 날씨, 뉴스, 일정 등을 종합하여 전달합니다."""
    return """
다음을 순서대로 실행하고, 실행한 결과를 사용자에게 알려주세요. 
첫째로 사용자가 위치한 도시를 파악하세요. 위치를 모른다면, 사용자에게 질문하세요.
둘째로 사용자의 위치를 기반으로 get_weather 도구를 호출하여 날씨 정보를 찾아서 제공합니다. 
셋째로 get_news_headlines 도구를 사용하여 오늘의 주요 뉴스를 출력합니다. 
ㄴ넷째로 get_exchange_rate 도구를 사용하여 환율 정보를 제공합니다.
다섯째로 get_kbo_rank 도구를 사용하여 현재 시간 프로야구 랭킹 및 전적을 리스트 형태로 출력합니다.  
여섯째로 today_schedule 도구를 사용하여 오늘 사용자의 일정을 알려줍니다. 
마지막으로 daily_quote 을 사용하여 명언을 출력하고, 따뜻한 말한마디를 덧붙입니다. 

출력은 다음과 같이 해주세요.
## 사용자님을 위한 맞춤 요약  
    
### 오늘의 날씨
[get_weather 의 결과]

### 오늘자 주요 뉴스
[get_news_headlines 의 결과] (링크를 함께 제공합니다)

### 환율 정보
[get_exchange_rate 의 결과]

### 야구단 랭킹 
[get_kbo_rank 의 결과]

### 오늘의 업무 일정
[today_schedule 의 결과]

### 영감을 주는 격언 한마디
[daily_quote 의 결과]
"""

