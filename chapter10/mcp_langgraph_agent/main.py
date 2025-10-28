"""FastAPI 메인 애플리케이션"""
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_core.messages import HumanMessage
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
import uvicorn

from config import FASTAPI_HOST, FASTAPI_PORT, MCP_SERVER_URL
from agent import create_agent

import dotenv
dotenv.load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI 애플리케이션의 생명주기 동안 MCP 연결 및 에이전트 설정을 관리합니다."""
    print("애플리케이션 시작: MCP 서버에 연결하고 에이전트를 설정합니다...")

    async with streamablehttp_client(MCP_SERVER_URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            app.state.agent_executor = create_agent(tools)
            print("에이전트 설정 완료. 애플리케이션이 준비되었습니다.")
            yield

    print("애플리케이션 종료.")
    app.state.agent_executor = None


# FastAPI 앱 인스턴스 생성
app = FastAPI(lifespan=lifespan)


async def stream_agent_response(agent_executor, message: str, session_id: str):
    """에이전트의 응답을 스트리밍하는 비동기 제너레이터"""
    if agent_executor is None:
        yield "에이전트가 아직 준비되지 않았습니다. 잠시 후 다시 시도해주세요."
        return

    try:
        config = {"configurable": {"thread_id": session_id}}
        input_message = HumanMessage(content=message)

        # astream_events를 사용하여 응답 스트리밍
        async for event in agent_executor.astream_events(
            {"messages": [input_message]},
            config=config,
            version="v1",
        ):
            kind = event["event"]
            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    # 스트리밍된 콘텐츠를 클라이언트로 전송
                    yield content
            elif kind == "on_tool_start":
                # TODO: 도구 사용 시작을 클라이언트에 알릴 수 있습니다.
                print(f"Tool start: {event['name']}")
            elif kind == "on_tool_end":
                # TODO: 도구 사용 완료를 클라이언트에 알릴 수 있습니다.
                print(f"Tool end: {event['name']}")
            else:
                print(event)

    except Exception as e:
        print(f"스트리밍 중 오류 발생: {e}")
        yield f"오류가 발생했습니다: {e}"


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """메인 채팅 페이지를 렌더링"""
    return HTMLResponse(content="Hello, World!")


@app.post("/chat")
async def chat(request: Request, message: str = Form(...), session_id: str = Form(...)):
    """사용자 메시지를 받아 에이전트의 응답을 스트리밍합니다."""
    agent_executor = request.app.state.agent_executor
    return StreamingResponse(
        stream_agent_response(agent_executor, message, session_id),
        media_type="text/event-stream",
    )


if __name__ == "__main__":
    uvicorn.run(app, host=FASTAPI_HOST, port=FASTAPI_PORT)
