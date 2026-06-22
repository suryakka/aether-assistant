import { create } from "zustand";

import type { ChatMessage, SessionStatus } from "../types";

interface SessionState {
  sessionId: string;
  status: SessionStatus;
  messages: ChatMessage[];
  streamingContent: string;
  error: string | null;
  setStatus: (status: SessionStatus) => void;
  addUserMessage: (content: string) => void;
  appendStreamChunk: (chunk: string) => void;
  finalizeAssistantMessage: (content: string) => void;
  setError: (error: string | null) => void;
  clearMessages: () => void;
  resetStream: () => void;
}

export const useSessionStore = create<SessionState>((set) => ({
  sessionId: crypto.randomUUID(),
  status: "connecting",
  messages: [],
  streamingContent: "",
  error: null,

  setStatus: (status) => set({ status }),

  addUserMessage: (content) =>
    set((state) => ({
      messages: [
        ...state.messages,
        { id: crypto.randomUUID(), role: "user", content },
      ],
      streamingContent: "",
      error: null,
    })),

  appendStreamChunk: (chunk) =>
    set((state) => ({
      streamingContent: state.streamingContent + chunk,
    })),

  finalizeAssistantMessage: (content) =>
    set((state) => ({
      messages: [
        ...state.messages,
        { id: crypto.randomUUID(), role: "assistant", content },
      ],
      streamingContent: "",
    })),

  setError: (error) => set({ error, status: "error" }),

  clearMessages: () =>
    set({ messages: [], streamingContent: "", error: null, status: "idle" }),

  resetStream: () => set({ streamingContent: "" }),
}));
