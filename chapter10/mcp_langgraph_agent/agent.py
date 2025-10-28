"""에이전트 생성 및 관리 모듈"""
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_openai import ChatOpenAI
from config import OPENAI_MODEL
from prompts import create_prompt_template


def create_agent(tools):
    """
    주어진 도구를 사용하여 에이전트를 생성합니다.
    
    Args:
        tools: 에이전트가 사용할 수 있는 도구 목록
        
    Returns:
        생성된 에이전트
    """
    memory = InMemorySaver()
    prompt = create_prompt_template()
    llm = ChatOpenAI(model=OPENAI_MODEL)
    return create_react_agent(llm, tools, checkpointer=memory, prompt=prompt)

