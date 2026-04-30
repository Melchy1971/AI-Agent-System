from fastapi import APIRouter, Depends
from api.dependencies import get_registry
from agent.tools.registry import ToolRegistry

router = APIRouter()


@router.get("/")
async def list_tools(registry: ToolRegistry = Depends(get_registry)):
    return {"tools": registry.list_names()}
