import re
from typing import Any

from langchain.agents.middleware import AgentMiddleware, AgentState, hook_config
from langgraph.runtime import Runtime

# table_users
# table_payments
# redact prefix "table_"

REDACTED_KEYS = [
    r"table_\w+",
]


# source:
class RedactionMiddleware(AgentMiddleware):
    # Redact sensitive information from the final output
    @hook_config(can_jump_to=["end"])
    def after_agent(self, state: AgentState, runtime: Runtime) -> dict[str, Any]:
        messages = state.get("messages") or []
        if not messages:
            return state

        last_message = messages[-1]
        content = last_message.content
        if not content:
            return state

        for pattern in REDACTED_KEYS:
            content = re.sub(pattern, "[REDACTED]", content)
        last_message.content = content
        return state
