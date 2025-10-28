# MCP LangGraph 에이전트

MCP (Model Context Protocol)와 LangGraph를 결합한 에이전트 시스템입니다.

## 프로젝트 구조

```
mcp_langgraph_agent/
├── config.py              # 애플리케이션 설정 관리
├── prompts.py             # 에이전트 프롬프트 템플릿
├── agent.py               # 에이전트 생성 로직
├── main.py                # FastAPI 메인 애플리케이션
├── mcp_server.py          # MCP 서버
├── app_streamlit.py       # Streamlit 클라이언트 UI
└── tools/                 # MCP 도구 모듈
    ├── __init__.py
    ├── web_tools.py       # 웹 스크래핑 도구
    ├── weather_tools.py   # 날씨 조회 도구
    ├── news_tools.py      # 뉴스 수집 도구
    ├── sports_tools.py    # 스포츠 정보 도구
    ├── schedule_tools.py  # 일정 관리 도구
    └── llm_tools.py       # LLM을 활용한 도구
```

## 주요 기능

### 1. MCP 도구들

- **웹 스크래핑**: 웹페이지의 텍스트 콘텐츠 추출
- **날씨 조회**: 도시 이름으로 현재 날씨 정보 조회
- **뉴스 수집**: 구글 뉴스 RSS 피드에서 최신 헤드라인 수집
- **야구 순위**: KBO 프로야구 팀 순위 조회
- **일정 관리**: 사용자의 오늘 일정 표시
- **명언 생성**: LLM을 활용한 오늘의 명언 출력
- **종합 브리핑**: 하루를 시작하는 종합 브리핑 제공

### 2. 에이전트 시스템

- LangGraph 기반의 ReAct 에이전트
- 여러 도구를 활용한 복합적인 작업 수행
- 스트리밍 응답 지원
- 대화 이력 관리

### 3. 클라이언트

- **FastAPI 기반 웹 UI**: HTML 템플릿 기반 채팅 인터페이스
- **Streamlit UI**: 대화형 웹 인터페이스

## 설치 및 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env` 파일에 필요한 환경 변수를 설정하세요.

### 3. MCP 서버 실행

```bash
python mcp_server.py
```

### 4. FastAPI 서버 실행

```bash
python main.py
```

### 5. Streamlit UI 실행 (선택사항)

```bash
streamlit run app_streamlit.py
```

## 사용 방법

### FastAPI 웹 UI 사용

1. MCP 서버 실행 (포트 8000)
2. FastAPI 서버 실행 (포트 8001)
3. 브라우저에서 `http://localhost:8001` 접속

### Streamlit UI 사용

1. MCP 서버 실행 (포트 8000)
2. FastAPI 서버 실행 (포트 8001)
3. Streamlit 앱 실행
4. 브라우저에서 Streamlit UI 접속

## 아키텍처

### 계층 구조

1. **도구 계층**: `tools/` 디렉토리의 각종 도구 모듈
2. **에이전트 계층**: LangGraph 기반 에이전트 시스템
3. **서버 계층**: FastAPI와 MCP 서버
4. **클라이언트 계층**: 웹 UI 및 Streamlit UI

### 데이터 흐름

```
사용자 입력 → FastAPI 서버 → LangGraph 에이전트 → MCP 서버 → 도구 실행 → 결과 반환
```

## 개발 가이드

### 새로운 도구 추가하기

1. `tools/` 디렉토리에 새로운 파일 생성 (예: `my_tools.py`)
2. 도구 함수 작성
3. `mcp_server.py`에서 도구를 MCP 서버에 등록

예시:

```python
# tools/my_tools.py
def my_tool() -> str:
    """도구 설명"""
    # 도구 로직
    return "result"

# mcp_server.py
from tools import my_tools

@mcp.tool()
def my_tool() -> str:
    """도구 설명"""
    return my_tools.my_tool()
```

### 프롬프트 수정하기

`prompts.py` 파일의 `get_system_prompt()` 함수를 수정하여 에이전트의 동작을 변경할 수 있습니다.

### 설정 변경하기

`config.py` 파일에서 애플리케이션 설정을 변경할 수 있습니다.

## 라이선스

MIT
