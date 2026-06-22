import { useCallback, useEffect, useRef } from "react";

import { useSessionStore } from "../store/sessionStore";
import type { SessionStatus, WSEvent } from "../types";
import { WS_BASE_URL } from "../types";

interface UseAetherWSOptions {
  sessionId: string;
  onEvent?: (event: WSEvent) => void;
}

export function useAetherWS({ sessionId, onEvent }: UseAetherWSOptions) {
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<number | null>(null);

  const setStatus = useSessionStore((s) => s.setStatus);
  const appendStreamChunk = useSessionStore((s) => s.appendStreamChunk);
  const finalizeAssistantMessage = useSessionStore((s) => s.finalizeAssistantMessage);
  const setError = useSessionStore((s) => s.setError);

  const handleEvent = useCallback(
    (event: WSEvent) => {
      onEvent?.(event);

      switch (event.type) {
        case "status":
          setStatus(event.data.status as SessionStatus);
          break;
        case "response_chunk":
          appendStreamChunk(String(event.data.content ?? ""));
          break;
        case "done":
          finalizeAssistantMessage(String(event.data.content ?? ""));
          break;
        case "error":
          setError(String(event.data.message ?? "Unknown error"));
          break;
      }
    },
    [onEvent, setStatus, appendStreamChunk, finalizeAssistantMessage, setError],
  );

  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) return;

    setStatus("connecting");
    const ws = new WebSocket(`${WS_BASE_URL}/ws/session/${sessionId}`);
    wsRef.current = ws;

    ws.onopen = () => {
      setStatus("idle");
      setError(null);
    };

    ws.onmessage = (msg) => {
      try {
        const event = JSON.parse(msg.data as string) as WSEvent;
        handleEvent(event);
      } catch {
        setError("Failed to parse server message");
      }
    };

    ws.onerror = () => {
      setStatus("disconnected");
      setError("WebSocket connection error");
    };

    ws.onclose = () => {
      setStatus("disconnected");
      reconnectTimeoutRef.current = window.setTimeout(connect, 3000);
    };
  }, [sessionId, handleEvent, setStatus, setError]);

  const sendQuery = useCallback((content: string) => {
    if (wsRef.current?.readyState !== WebSocket.OPEN) {
      setError("Not connected to backend");
      return;
    }
    wsRef.current.send(JSON.stringify({ type: "query", content }));
  }, [setError]);

  const sendClear = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ type: "clear" }));
    }
  }, []);

  useEffect(() => {
    connect();
    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      wsRef.current?.close();
    };
  }, [connect]);

  return { sendQuery, sendClear, reconnect: connect };
}
