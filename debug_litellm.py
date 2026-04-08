import litellm
import json
import os

litellm.drop_params = False
litellm.modify_params = True # As we set it

print(litellm._turn_on_debug())
messages = [{"role": "user", "content": "test"}]
kwargs = {"thinking": {"type": "enabled", "budget_tokens": 1024}, "temperature": 1.0}

try:
    # Try an offline mock to just see payload formatting if possible
    # litellm will fail connecting but might print the request
    litellm.completion("anthropic/claude-opus-4-5-mock", messages, api_base="http://127.0.0.1:9999", **kwargs)
except Exception as e:
    pass
