import litellm

# Enable automatic parameter modification
litellm.modify_params = True

# Now this will work even if thinking_blocks are missing from the assistant message
response = litellm.completion(
    model="anthropic/claude-opus-4-5-20251101-hz",
    thinking={"type": "enabled", "budget_tokens": 1024},
    tools=[...],
    messages=[
        {"role": "user", "content": "What's the weather in Madrid?"},
        {
            "role": "assistant",
            "tool_calls": [{"id": "call_123", "type": "function", "function": {"name": "get_weather", "arguments": '{"city": "Madrid"}'}}]
            # Note: thinking_blocks is missing here - LiteLLM will handle it
        },
        {"role": "tool", "tool_call_id": "call_123", "content": "22°C sunny"}
    ]
)
