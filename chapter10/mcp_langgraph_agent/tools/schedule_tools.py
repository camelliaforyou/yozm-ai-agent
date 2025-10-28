"""일정 관련 도구"""


def today_schedule() -> str:
    """임의의 스케줄을 반환합니다."""
    events = ["10:00 팀 미팅", "13:00 점심 약속", "15:00 프로젝트 회의", "19:00 헬스장"]
    return " | ".join(events)

