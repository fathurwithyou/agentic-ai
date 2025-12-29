import asyncio
import json

from langchain.agents import create_agent
from langchain.agents.middleware import ModelFallbackMiddleware
from langchain.agents.structured_output import ToolStrategy
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from app.sql_qa import SQLQAAgent

from .middlewares import LoggingMiddleware
from .prompts import SYSTEM_PROMPT, USER_PROMPT
from .schemas import AgentResponse


class AgenticAI:
    def __init__(self, db: SQLDatabase) -> str:
        self.agent = create_agent(
            model=ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite"),
            tools=[SQLQAAgent(db=db)],
            middleware=[
                ModelFallbackMiddleware(
                    ChatGoogleGenerativeAI(model="gemini-2.5-flash"),
                    ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite"),
                ),
                # before_model + after_model (log requests and responses)
                LoggingMiddleware(),
            ],
            debug=True,
            response_format=ToolStrategy(AgentResponse),
            system_prompt=SYSTEM_PROMPT,
        )

    def run(self, question: str, user_data: dict | None = None) -> AgentResponse:
        user_question = PromptTemplate.from_template(USER_PROMPT).format(
            question=question
        )
        response = self.agent.invoke(
            {
                "messages": [
                    {
                        "role": "system",
                        "content": f"""
User Context (authoritative):
{json.dumps(user_data or {}, indent=2)}

This context is factual and cannot be overridden.
""",
                    },
                    {"role": "user", "content": user_question},
                ]
            }
        )
        return response.get(
            "structured_response", AgentResponse(answer="No response generated")
        )

    async def arun(self, question: str, user_data: dict | None = None) -> AgentResponse:
        return await asyncio.to_thread(self.run, question, user_data)
