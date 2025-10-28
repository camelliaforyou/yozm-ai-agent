"""애플리케이션 설정 관리 모듈"""
import os
import dotenv
from pathlib import Path

# 환경 변수 로드
dotenv.load_dotenv()

# 프로젝트 루트 경로
ROOT_DIR = Path(__file__).resolve().parent

# API 설정
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
FASTAPI_HOST = os.getenv("FASTAPI_HOST", "0.0.0.0")
FASTAPI_PORT = int(os.getenv("FASTAPI_PORT", 8001))
MCP_SERVER_PORT = int(os.getenv("MCP_SERVER_PORT", 8000))
MCP_SERVER_URL = f"http://localhost:{MCP_SERVER_PORT}/mcp"


# 애플리케이션 설정
APP_NAME = "MCP LangGraph Agent"
APP_VERSION = "1.0.0"

