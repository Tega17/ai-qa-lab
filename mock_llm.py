import json


def mock_llm(prompt: str, mode: str = "normal") -> str:
    if mode == "broken_json":
        return '{"status": "shipped", "order_id": "1042"'  # missing closing brace

    if mode == "missing_field":
        return json.dumps({"order_id": "1042"})  # missing 'status'

    if mode == "too_wordy":
        return json.dumps({
            "order_id": "1042",
            "status": "shipped",
            "notes": "Your package left the warehouse today and is currently traveling across the regional delivery network with tracking updates every few hours."
        })

    if "JSON" in prompt or "json" in prompt:
        return json.dumps({"action": "reset", "target": "password", "steps": 2})

    if "30 days" in prompt or "refund" in prompt.lower():
        return json.dumps({"policy": "Refunds allowed within 30 days of delivery."})

    return json.dumps({"order_id": "1042", "status": "shipped"})