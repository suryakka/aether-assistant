export type SessionStatus =
  | "idle"
  | "listening"
  | "watching"
  | "thinking"
  | "researching"
  | "executing"
  | "done"
  | "error"
  | "connecting"
  | "disconnected";

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
}

export interface WSEvent {
  type: string;
  data: Record<string, unknown>;
}

export const BACKEND_URL = "http://127.0.0.1:8787";
export const WS_BASE_URL = "ws://127.0.0.1:8787";

export function createSessionId(): string {
  return crypto.randomUUID();
}
