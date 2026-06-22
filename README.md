# Aether Assistant

Local-first AI desktop assistant — privacy-first, offline-capable, cross-platform.

**Personal project** by [suryakka](https://github.com/suryakka).

## Stack

- **Frontend:** Tauri 2 + React + TypeScript
- **Backend:** Python FastAPI (sidecar)
- **LLM:** Ollama (local inference)
- **STT:** Silero VAD + faster-whisper (EN + ID)

## Project structure

```
aether-assistant/
├── apps/
│   ├── desktop/     # Tauri + React overlay UI
│   └── backend/     # Python FastAPI services
├── packages/        # Shared SDK & types (planned)
├── plugins/         # Optional plugins (planned)
├── docker/          # Dev environment (planned)
└── scripts/         # Build & dev scripts
```

## Development

### Prerequisites

- Node.js 20+, pnpm
- Rust (for Tauri)
- Python 3.11+
- [Ollama](https://ollama.com) (for local LLM)

### Desktop app

```bash
cd apps/desktop
pnpm install
pnpm tauri dev
```

### Backend (planned)

```bash
cd apps/backend
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
uvicorn aether.main:app --reload --port 8787
```

## License

MIT
