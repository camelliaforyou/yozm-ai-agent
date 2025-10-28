"""환율 관련 도구"""
import httpx

def get_exchange_rate(base: str = "USD", target: str = "KRW") -> str:
    """기준 통화 대비 환율을 조회합니다 (Open ER API)."""
    try:
        url = f"https://open.er-api.com/v6/latest/{base}"
        resp = httpx.get(url, timeout=10)
        data = resp.json()

        if data.get("result") != "success":
            return f"환율 정보를 가져오지 못했습니다. ({data.get('error-type', 'unknown error')})"

        rate = data["rates"].get(target)
        if rate:
            return f"{base} → {target}: {rate:,.2f}"
        else:
            return f"{target}에 대한 환율 정보를 찾을 수 없습니다."
    except Exception as e:
        return f"환율 조회 중 오류 발생: {e}"
