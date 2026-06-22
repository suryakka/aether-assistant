#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="$ROOT/apps/backend"
DESKTOP_DIR="$ROOT/apps/desktop"

cleanup() {
  echo ""
  echo "Shutting down..."
  kill "$BACKEND_PID" 2>/dev/null || true
  kill "$DESKTOP_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

echo "Starting Aether backend on :8787..."
cd "$BACKEND_DIR"
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -e ".[dev]" -q
else
  source .venv/bin/activate
fi

uvicorn aether.main:app --reload --host 127.0.0.1 --port 8787 &
BACKEND_PID=$!

echo "Waiting for backend..."
for i in $(seq 1 20); do
  if curl -sf http://127.0.0.1:8787/health > /dev/null 2>&1; then
    echo "Backend ready."
    break
  fi
  sleep 0.5
done

echo "Starting Aether desktop (Tauri)..."
cd "$DESKTOP_DIR"
if [ ! -d "node_modules" ]; then
  pnpm install
fi

source "$HOME/.cargo/env" 2>/dev/null || true
pnpm tauri dev &
DESKTOP_PID=$!

wait "$DESKTOP_PID"
