import requests

try:
    response = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={
            "model": "llama3.2:latest",
            "prompt": "Test prompt",
            "options": {"max_tokens": 150, "temperature": 0.7}
        },
        timeout=10
    )
    response.raise_for_status()
    print("Success:", response.json())
except Exception as e:
    print("Error:", e)
