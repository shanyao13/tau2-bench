import requests
import json

api_base = "http://10.200.95.16:30300/v1/chat/completions"

def test_model(model_name):
    payload = {
        "model": model_name,
        "messages": [
            {"role": "user", "content": "What is the capital of France? Please think step by step."}
        ],
        "reasoning_effort": "low",
        "temperature": 1.0,
        "max_tokens": 8000
    }
    print(f"\n--- Testing model: {model_name} ---")
    try:
        response = requests.post(api_base, json=payload, headers={"Content-Type": "application/json"})
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            res_json = response.json()
            # print("Full Response:")
            # print(json.dumps(res_json, indent=2))
            
            msg = res_json.get("choices", [{}])[0].get("message", {})
            has_think = msg.get("reasoning_content") is not None or "thinking_blocks" in msg or "<think>" in msg.get("content", "")
            print(f"Content length: {len(msg.get('content', ''))}")
            print(f"Has reasoning_content: {msg.get('reasoning_content') is not None}")
            print(f"Has thinking_blocks: {'thinking_blocks' in msg}")
            print(f"Content snippet: {msg.get('content', '')[:100]}...")
            if msg.get("reasoning_content"):
                print(f"Reasoning snippet: {msg.get('reasoning_content')[:100]}...")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

test_model("anthropic/claude-3-7-sonnet-20250219")
test_model("anthropic/claude-opus-4-5-20251101-hz")
