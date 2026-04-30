# Project: AI-Agent-System

**Status:** v0.1.0 stabil — 42/42 Tests grün (2026-04-30)
**Stack:** Python 3.10+, FastAPI, Anthropic, ChromaDB, SQLAlchemy, pytest, Pydantic v2

## Architektur
| Layer | Module | Status |
|-------|--------|--------|
| Core loop | agent/core/ | ✓ produktionsreif |
| Tools | agent/tools/ | ✓ AST-Calculator, FileHandler, WebSearch, DB |
| LLM providers | llm/providers/ | ✓ OpenAI, Anthropic, Local/Ollama |
| Memory | memory/ | ✓ ShortTermBuffer, LongTermStore, VectorDB |
| API | api/ | ✓ FastAPI, Routes, Controllers |
| Config | config/ | ✓ pydantic-settings, YAML |
| Dashboard | agent_dashboard.html | ✓ Mock-Daten, bereit für API-Verdrahtung |

## Datenmodelle (Pydantic v2)
- `PlanAction` — step, description, tool_name, args
- `ToolCall` — call_id (uuid), tool_name, args, timestamp
- `ToolResult` — call_id, success, output, error, duration_ms
- `AgentStep` — step_number, action, tool_call, result
- `AgentState` — run_id, task, status, plan, steps, final_response

## Sicherheit
- Calculator: kein eval() — AST-Walker mit Whitelist (ast.BinOp, ast.UnaryOp, 6 Funktionen)
- Executor: fängt ValueError und Exception separat, crasht nie
- Planner: invalides JSON → Fallback, kein Crash
- Loop-Detection: MD5-Fingerprint über (tool_name, args), Fenster 3

## Offene Punkte
- .env mit API-Keys befüllen
- sentence-transformers lokal installieren (Sandbox-Timeout)
- FastAPI-Server mit realem LLM testen
- Dashboard gegen echte /agent/run API verdrahten
