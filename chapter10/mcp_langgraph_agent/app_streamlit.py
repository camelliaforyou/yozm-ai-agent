"""Streamlit 클라이언트 UI"""
import os
import time
import requests
import streamlit as st

FASTAPI_URL = os.getenv("BACKEND_URL", "http://localhost:8001/chat")

st.set_page_config(page_title="MCP LangGraph 에이전트", page_icon="🤖", layout="wide")
st.title("🤖 MCP LangGraph 에이전트 (Streamlit UI)")

# ===== 세션 상태 =====
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = f"session_{int(time.time()*1000)}"


# ====== 함수 분리 ======
def process_message(user_text: str):
    """입력된 메시지를 FastAPI에 전달하고 결과 출력"""
    # 1️⃣ 사용자 메시지 출력
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    # 2️⃣ 봇 응답
    with st.chat_message("assistant"):
        placeholder = st.empty()
        acc = ""
        with st.spinner("AI가 응답 중입니다..."):
            try:
                resp = requests.post(
                    FASTAPI_URL,
                    data={"message": user_text, "session_id": st.session_state.session_id},
                    stream=True,
                    timeout=60,
                )
                resp.raise_for_status()
                for chunk in resp.iter_content(chunk_size=None):
                    if not chunk:
                        continue
                    acc += chunk.decode("utf-8")
                    placeholder.markdown(acc + "▌")
                    time.sleep(0.02)
            except requests.RequestException as e:
                acc = f"❌ 오류 발생: {e}"
                placeholder.markdown(acc)

        placeholder.markdown(acc)
        st.session_state.messages.append({"role": "assistant", "content": acc})


# ===== 기존 히스토리 렌더 =====
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# ===== 사이드바 =====
with st.sidebar:
    st.header("⚙️ 설정")
    st.subheader("🧩 빠른 명령")

    if st.button("오늘 브리핑 요청"):
        st.session_state["auto_prompt"] = "오늘 브리핑 해줘"
    if st.button("뉴스 요약 보기"):
        st.session_state["auto_prompt"] = "오늘 주요 뉴스 요약해줘"
    if st.button("명언 듣기"):
        st.session_state["auto_prompt"] = "오늘의 명언 알려줘"
    if st.button("환율 보기 (USD→KRW)"):
        st.session_state["auto_prompt"] = "환율 알려줘"

    st.markdown("---")
    if st.button("대화 초기화"):
        st.session_state.messages = []
        st.session_state.session_id = f"session_{int(time.time()*1000)}"
        st.rerun()

# ===== 본문 =====
# 기존 채팅 기록 출력
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# 입력 또는 버튼 자동 입력
prompt = st.chat_input("메시지를 입력하세요… (Shift+Enter 줄바꿈)")
auto_prompt = st.session_state.pop("auto_prompt", None) if "auto_prompt" in st.session_state else None

if prompt or auto_prompt:
    process_message(prompt or auto_prompt)

    st.caption("백엔드 URL")
    st.code(FASTAPI_URL, language="bash")
