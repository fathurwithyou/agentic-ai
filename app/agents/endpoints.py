from fastapi import APIRouter
from .schemas import QARequest, QAResponse
from .agent import AgenticAI
from app.shared.database import mysql_engine
import time

router = APIRouter(prefix="/agent", tags=["Agent"])

@router.post("/ask", response_model=QAResponse)
async def ask_question(request: QARequest) -> QAResponse:
    agent = AgenticAI(db=mysql_engine)
    st_time = time.perf_counter()
    response = await agent.arun(request.question)
    return QAResponse(answer=response.answer, time=time.perf_counter() - st_time)