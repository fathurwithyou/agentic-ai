from pydantic import BaseModel
from langchain.agents.middleware import AgentMiddleware, before_agent, AgentState
from langgraph.runtime import Runtime
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain.messages import AIMessage
from langchain.agents.structured_output import ToolStrategy
from langchain_core.prompts import PromptTemplate
from typing import Literal

CHECK_VIOLATION_PROMPT = """
You are a data governance and routing agent.

## Input
**User Question:**
{{ question }}

## Task
Classify the question into exactly one label:
- CLEAR      → valid, relevant, safe → continue to SQL-QA
- VIOLATION  → sensitive OR irrelevant → skip and end

## VIOLATION if the question
- Requests sensitive data:
  - PII (email, phone, address, national/employee ID, DOB)
  - Salary, compensation, HR data tied to individuals
  - Passwords, tokens, API keys, credentials
  - Financial or legal data tied to individuals
- Is NOT a meaningful data question:
  - Off-topic, nonsensical, or conversational
  - Unrelated to databases, analytics, or business data
  - Cannot reasonably map to a data query

## CLEAR if the question
- Is a valid data-related question
- Targets non-sensitive, business-level information
- Can reasonably be answered via SQL over allowed data

## Output Rules
- Output exactly one word: **CLEAR** or **VIOLATION**
- No explanations
- No punctuation
"""


class AnswerModel(BaseModel):
    result: Literal["VIOLATION", "CLEAR"]


class BeforeAgentMiddleware(AgentMiddleware):
    @before_agent(can_jump_to="end")
    def check_sensitive_input(state: AgentState, runtime: Runtime) -> dict[str, any]:
        agent = create_agent(
            model=ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite"),
            response_format=ToolStrategy(AnswerModel),
        )
        response = agent.invoke(
            {
                "input": PromptTemplate.from_template(CHECK_VIOLATION_PROMPT).format(
                    question=state.get("messages")[0].content
                )
            }
        )
        result = response.get("structured_response")
        if result and result.result == "VIOLATION":
            return {
                "messages": [
                    AIMessage(
                        "Your question has been identified as violating data governance policies and cannot be processed."
                    )
                ],
                "jump_to": "end",
                "structured_response": "Your question has been identified as violating data governance policies and cannot be processed.",
            }
        return state
