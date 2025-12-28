from .middlewares import (
    BeforeAgentMiddleware,
    AfterAgentMiddleware,

)
from .tools import *  # noqa
from .schemas import AgentSQLResponse
from .prompts import SYSTEM_PROMPT

import asyncio
from langchain.agents import create_agent
from langchain.agents.middleware import ModelFallbackMiddleware
from langchain.agents.structured_output import ToolStrategy
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import BaseTool
from langchain_community.tools.sql_database.tool import (
    ListSQLDatabaseTool,
    QuerySQLDatabaseTool,
    InfoSQLDatabaseTool
)
from langchain_community.utilities.sql_database import SQLDatabase

from langchain_core.prompts import PromptTemplate


class SQLQAAgent(BaseTool):
    def __init__(self, db: SQLDatabase):
        self.agent = create_agent(
            model=ChatGoogleGenerativeAI(model="gemini-3-flash-preview"),
            tools=[
                ListSQLDatabaseTool(db=db),
                QuerySQLDatabaseTool(db=db),
                InfoSQLDatabaseTool(db=db),
            ],
            middleware=[
                ModelFallbackMiddleware(
                    ChatGoogleGenerativeAI(model="gemini-2.5-flash"),
                    ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite"),
                ),
                # before agent (guardrail before)
                BeforeAgentMiddleware(),
                # TODO: before model 
                # TODO: after model (logging, input-output, supervisor agent?)
                # after agent (guardrail after)
                AfterAgentMiddleware(),
            ],
            debug=True,
            response_format=ToolStrategy(AgentSQLResponse),
        )

    def _run(self, question: str, user_data: dict) -> AgentSQLResponse:
        prompt_template = PromptTemplate.from_template(SYSTEM_PROMPT).format(question=question, user_data=user_data)
        return self.agent.invoke({"input": prompt_template})["structured_response"]

    async def _arun(self, question: str, user_data: dict) -> AgentSQLResponse:
        return await asyncio.run(self._run(question, user_data))
