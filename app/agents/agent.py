import asyncio

from langchain.agents import create_agent
from langchain.agents.middleware import ModelFallbackMiddleware
from langchain.agents.structured_output import ToolStrategy
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI

from app.sql_qa import SQLQAAgent

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
            ],
            debug=True,
            response_format=ToolStrategy(AgentResponse),
        )

    def run(self, question: str) -> AgentResponse:
        response = self.agent.invoke(
            {"messages": [{"role": "user", "content": question}]}
        )
        return response.get(
            "structured_response", AgentResponse(answer="No response generated")
        )

    async def arun(self, question: str) -> AgentResponse:
        return await asyncio.to_thread(self.run, question)
