from pydantic import BaseModel, Field, ConfigDict

# For endpoint request
class QARequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    question: str = Field(..., description="The question to be answered.")

class QAResponse(BaseModel):
    answer: str = Field(..., description="The answer to the question.")
    time: float = Field(..., description="Time taken to generate the answer in seconds.")

class AgentResponse(BaseModel):
    answer: str = Field(..., description="The final answer to the question.")