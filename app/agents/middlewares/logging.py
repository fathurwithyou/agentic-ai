import logging
from typing import Any

from langchain.agents.middleware import AgentMiddleware, AgentState
from langgraph.runtime import Runtime


class LoggingMiddleware(AgentMiddleware):
    def before_model(
        self, state: AgentState, runtime: Runtime
    ) -> dict[str, Any] | None:
        messages = state.get("messages")
        if messages:
            last_message = messages[-1]
            logging.info("Main Agent - Message sent to model: %s", last_message.content)
        return None

    def after_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        messages = state.get("messages")
        if messages:
            last_message = messages[-1]
            logging.info("Main Agent - Response from model: %s", last_message.content)
        else:
            logging.info("Main Agent - No messages found in state")
        return None
