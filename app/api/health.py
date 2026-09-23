from datetime import datetime, timezone

def handler(request):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json; charset=utf-8"
        },
        "body": __import__("json").dumps({
            "ok": True,
            "service": "kfood-trend-api",
            "time": datetime.now(timezone.utc).isoformat()
        })
    }
