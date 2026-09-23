import os
from datetime import datetime, timezone
from .db import save_entities, save_signal

# 이 파일은 "수집 오케스트레이터"입니다.
# 실제 API 호출은 각 source collector로 분리합니다.
# API Key가 없는 소스는 호출하지 않고 skipped 처리합니다.

def run_collection():
    started = datetime.now(timezone.utc).isoformat()
    results = []

    sources = [
        ("tiktok", "TIKTOK_API_KEY"),
        ("instagram", "META_ACCESS_TOKEN"),
        ("qoo10", "QOO10_API_KEY"),
    ]

    # 현재 단계에서는 외부 API를 임의로 호출하지 않습니다.
    # 실제 승인된 API 스펙을 확인한 뒤 각 collector를 연결합니다.
    for source, env_name in sources:
        results.append({
            "source": source,
            "status": "configured" if os.getenv(env_name) else "skipped",
            "credential": env_name
        })

    # Google Trends는 별도 공급원/접근 방식이 확정된 뒤 연결합니다.
    return {
        "ok": True,
        "started_at": started,
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "results": results
    }
