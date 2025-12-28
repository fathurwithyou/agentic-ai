from langchain.agents.middleware import AgentMiddleware, after_agent, AgentState
from langgraph.runtime import Runtime
import re

# table_users
# table_payments
# redact prefix "table_"

REDACTED_KEYS = [
    r"table_\w+",
]


# source:
class AfterAgentMiddleware(AgentMiddleware):
    # Redact sensitive information from the final output
    @after_agent(can_jump_to="end")
    def redact_output(state: AgentState, runtime: Runtime) -> dict[str, any]:
        last_message = state.get("messages")[-1].content
        if last_message:
            redacted_message = last_message
            for pattern in REDACTED_KEYS:
                redacted_message = re.sub(pattern, "[REDACTED]", redacted_message)
            state.get("messages")[-1].content = redacted_message
        return state
