# AI Agent System

Modular autonomous agent framework: plan → execute → reflect.

## Architecture

```
agent/core      → AgentState, Planner, Executor, MemoryManager
agent/tools     → BaseTool, ToolRegistry, concrete tools
agent/prompts   → PromptLoader + templates
agent/workflows → TaskFlow, MultiStepFlow, ResearchFlow
llm/            → Provider abstraction (OpenAI, Anthropic, local)
memory/         → ShortTermBuffer, LongTermStore, VectorDB
api/            → FastAPI server, routes, controllers
config/         → Settings (pydantic-settings), YAML config
```

## Setup

```bash
cp .env.example .env
# Fill in API keys in .env

pip install -r requirements.txt
```

## Run

```bash
# CLI
python scripts/run_agent.py "Search for the latest news on AI agents"

# API server
uvicorn api.server:create_app --factory --host 0.0.0.0 --port 8000

# Seed vector memory
python scripts/seed_memory.py

# Reset all storage
python scripts/reset_storage.py
```

## Test

```bash
pytest tests/ -v --cov=agent --cov=llm --cov=memory --cov=api
```

## Adding a Tool

1. Create `agent/tools/my_tool.py` extending `BaseTool`
2. Register in `api/dependencies.py` → `get_registry()`
3. Add to `config/config.yaml` → `tools.enabled`

## Adding a Provider

1. Create `llm/providers/my_provider.py` extending `BaseProvider`
2. Implement `complete()` and `chat()`
3. Wire in `api/dependencies.py` → `get_llm()`
