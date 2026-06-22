# Aether Assistant

Local-first AI desktop assistant — privacy-first, offline-capable, cross-platform.

**Personal project** by [suryakka](https://github.com/suryakka) · [github.com/suryakka/aether-assistant](https://github.com/suryakka/aether-assistant)

## Features (Phase 1)

- Floating overlay UI with dark mode
- Global shortcut `Alt+Space` to toggle visibility
- Streaming chat via local Ollama (default: `qwen3:8b`)
- WebSocket real-time communication
- Clean Architecture Python backend

## Stack

| Layer | Tech |
|---|---|
| Desktop | Tauri 2 + React + TypeScript + Tailwind |
| Backend | Python FastAPI + WebSocket |
| LLM | Ollama (local inference) |

## Quick start

### Prerequisites

- Node.js 20+, pnpm
- Rust ([rustup.rs](https://rustup.rs))
- Python 3.11+
- [Ollama](https://ollama.com) with model pulled:

```bash
brew install ollama
ollama pull qwen3:8b
```

### Run (dev)

```bash
# Terminal 1 — backend
cd apps/backend
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
uvicorn aether.main:app --reload --port 8787

# Terminal 2 — desktop
cd apps/desktop
pnpm install
pnpm tauri dev
```

Or use the combined script:

```bash
bash scripts/dev.sh
```

### Docker Ollama (optional)

Native Ollama is recommended on Apple Silicon. For Linux/CI:

```bash
docker compose -f docker/docker-compose.dev.yml up -d
```

## Project structure

```
aether-assistant/
├── apps/
│   ├── desktop/          # Tauri + React overlay
│   └── backend/          # FastAPI Clean Architecture
├── docker/               # Dev services
├── scripts/              # dev.sh
└── .github/workflows/    # CI
```

## Backend architecture

```
aether/
├── domain/               # Entities + ports
├── application/          # Use cases
├── infrastructure/       # Ollama adapter, logging
├── presentation/         # REST + WebSocket
└── container.py          # Dependency injection
```

## Tests

```bash
cd apps/backend && pytest -v
cd apps/desktop && pnpm lint
```

## License

MIT
