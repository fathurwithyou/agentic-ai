import asyncio
from typing import Any

from langchain.agents import create_agent
from langchain.agents.middleware import ModelFallbackMiddleware
from langchain.agents.structured_output import ToolStrategy
from langchain.tools import BaseTool
from langchain_community.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
    QuerySQLDatabaseTool,
)
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field, PrivateAttr

from .middlewares import (
    AfterAgentMiddleware,
    BeforeAgentMiddleware,
)
from .prompts import SYSTEM_PROMPT
from .schemas import AgentSQLResponse


class SQLQAInput(BaseModel):
    question: str = Field(..., description="The question to answer.")
    user_data: dict | None = Field(default=None, description="Optional user context.")


class SQLQAAgent(BaseTool):
    name: str = "sql_qa"
    description: str = "Answer questions by querying the configured SQL database."
    args_schema: type[BaseModel] = SQLQAInput
    _agent: Any = PrivateAttr()

    def __init__(self, db: SQLDatabase):
        super().__init__()
        self._agent = create_agent(
            model=ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite"),
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

    def _run(self, question: str, user_data: dict | None = None) -> AgentSQLResponse:
        prompt_template = PromptTemplate.from_template(SYSTEM_PROMPT).format(
            question=question,
            user_data=user_data or {},
        )
        return self._agent.invoke(
            {"messages": [{"role": "user", "content": prompt_template}]}
        )["structured_response"]

    async def _arun(
        self, question: str, user_data: dict | None = None
    ) -> AgentSQLResponse:
        return await asyncio.to_thread(self._run, question, user_data)
