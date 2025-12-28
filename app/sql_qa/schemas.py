from pydantic import BaseModel, Field


# For agent response formatting
class AgentSQLResponse(BaseModel):
    answer: str = Field(..., description="The final answer to the question.")
