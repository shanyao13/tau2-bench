import sys
import os
sys.path.insert(0, os.path.abspath("src"))
import litellm
litellm._turn_on_debug()
from tau2.utils.llm_utils import generate
from tau2.data_model.message import UserMessage

# litellm.drop_params = False has been applied to llm_utils.py

try:
    generate(
        model="anthropic/claude-opus-4-5-20251101-hz",
        messages=[UserMessage(role="user", content="Hello")],
        api_base="http://10.200.95.16:30300",
        reasoning_effort="low",
        max_tokens=65536
    )
except Exception as e:
    print(f"Error: {e}")
