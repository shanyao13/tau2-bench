import litellm
import json
import dataclasses

# Apply the same monkeypatches from tau2
litellm.drop_params = False
original = litellm.supports_reasoning
def patched(model, *args, **kwargs):
    if "claude" in model or "anthropic/" in model: return True
    return original(model, *args, **kwargs)
litellm.supports_reasoning = patched
if hasattr(litellm, "utils"):
    litellm.utils.supports_reasoning = patched

from litellm.llms.anthropic.chat.handler import AnthropicChatCompletion

class DummyClient:
    def post(self, url, headers=None, data=None):
        print("--- REQUEST PAYLOAD ---")
        if isinstance(data, str):
            print(json.dumps(json.loads(data), indent=2))
        else:
            print(json.dumps(data, indent=2))
        raise Exception("done")
    
client = DummyClient()

anthropic = AnthropicChatCompletion()
try:
    anthropic.completion(
        model="claude-opus-4-5-20251101-hz",
        messages=[{"role": "user", "content": "hi"}],
        api_base="http://10.200.95.16:30300",
        api_key="sk-test",
        optional_params={"thinking": {"type": "enabled", "budget_tokens": 4096}, "temperature": 1.0},
        litellm_params={"model": "anthropic/claude-opus-4-5-20251101-hz"},
        client=client,
        custom_prompt_dict={},
        model_response=litellm.ModelResponse(),
        print_verbose=lambda *args: None,
        logging_obj=None,
        headers={},
        timeout=10,
    )
except Exception as e:
    if "done" not in str(e):
        print(e)

