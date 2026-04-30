# Tasks

## In Progress

## Todo
- [ ] .env befüllen mit API-Keys (ANTHROPIC_API_KEY, OPENAI_API_KEY)
- [ ] sentence-transformers lokal installieren (außerhalb Sandbox)
- [ ] AnthropicProvider gegen echte API testen
- [ ] FastAPI-Server starten und /agent/run mit realem LLM testen
- [ ] Dashboard (agent_dashboard.html) mit echten API-Daten verdrahten (fetch() gegen GET /agent/executions)
- [ ] web_search Tool testen (duckduckgo-search installiert?)
- [ ] DatabaseTool mit konkretem Connection String konfigurieren

## Done
- [x] Projektstruktur anlegen: 78 Dateien, vollständige Ordnerstruktur (2026-04-30)
- [x] Alle Python-Module mit funktionalem Code befüllen (2026-04-30)
- [x] Dependencies installieren via pip in Batches (2026-04-30)
- [x] Pydantic-Modelle: PlanAction, ToolCall, ToolResult, AgentState, AgentStep (2026-04-30)
- [x] Calculator auf AST-basiertem Parser umgestellt — kein eval() mehr (2026-04-30)
- [x] BaseTool: input_schema, output_schema, validate_input(), execute() (2026-04-30)
- [x] ToolRegistry: exists(), list_tools(), schema_summary(), all_schemas() (2026-04-30)
- [x] Planner: JSON-Output, Markdown-Strip, Registry-Validation, Fallback (2026-04-30)
- [x] Executor: immer ToolResult zurück, getrennte Exception-Handler, duration_ms (2026-04-30)
- [x] Agent Loop: Loop-Detection, max_steps, final_response (2026-04-30)
- [x] Logging: strukturiertes YAML-Config, agent/core/logger.py (2026-04-30)
- [x] 42 Tests — 42 passed, 0 failed (2026-04-30)
- [x] End-to-end run_agent.py mit MockLLM: "What is 25 * 12 + 5?" → 305.0 (2026-04-30)
- [x] Produktivitätssystem initialisiert: TASKS.md, CLAUDE.md, memory/, dashboard.html (2026-04-30)
- [x] Dashboard (agent_dashboard.html) erstellt — precision-instrument Aesthetic (2026-04-30)
