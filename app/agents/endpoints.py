import time

from fastapi import APIRouter

from app.shared.database import mysql_db

from .agent import AgenticAI
from .schemas import QARequest, QAResponse

router = APIRouter(prefix="/agent", tags=["Agent"])


@router.post("/ask", response_model=QAResponse)
async def ask_question(request: QARequest) -> QAResponse:
    agent = AgenticAI(db=mysql_db)
    st_time = time.perf_counter()
    response = await agent.arun(request.question, request.user_data)
    return QAResponse(answer=response.answer, time=time.perf_counter() - st_time)
