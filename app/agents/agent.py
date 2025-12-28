from langchain.agents import create_agent
from langchain.agents.middleware import ModelFallbackMiddleware
from langchain.agents.structured_output import ToolStrategy
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities.sql_database import SQLDatabase

from .schemas import AgentResponse
from app.sql_qa import SQLQAAgent
import asyncio

class AgenticAI:
    def __init__(self, db: SQLDatabase) -> str:
        self.agent = create_agent(
            model=ChatGoogleGenerativeAI(model="gemini-3-flash-preview"),
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
        response = self.agent.invoke({"input": question})
        return response["structured_response"]
    
    async def arun(self, question: str) -> AgentResponse:
        return await asyncio.run(self.run(question))