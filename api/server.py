from fastapi import FastAPI
from api.routes.agent_routes import router as agent_router
from api.routes.tool_routes import router as tool_router
from api.routes.memory_routes import router as memory_router


def create_app() -> FastAPI:
    app = FastAPI(title="AI Agent System", version="0.1.0")
    app.include_router(agent_router, prefix="/agent", tags=["agent"])
    app.include_router(tool_router, prefix="/tools", tags=["tools"])
    app.include_router(memory_router, prefix="/memory", tags=["memory"])
    return app
