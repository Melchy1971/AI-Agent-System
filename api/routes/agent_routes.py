from fastapi import APIRouter, Depends
from pydantic import BaseModel
from api.dependencies import get_agent
from agent.core.agent import Agent
from agent.core.state import AgentState

router = APIRouter()


class TaskRequest(BaseModel):
    task: str


@router.post("/run", response_model=dict)
async def run_task(req: TaskRequest, agent: Agent = Depends(get_agent)):
    state: AgentState = agent.run(req.task)
    return {"status": state.status, "results": state.results, "error": state.error}
