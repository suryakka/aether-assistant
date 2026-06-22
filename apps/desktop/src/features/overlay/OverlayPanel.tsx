import { useSessionStore } from "../../shared/store/sessionStore";
import { useAetherWS } from "../../shared/hooks/useAetherWS";
import { ChatInput } from "./ChatInput";
import { MessageStream } from "./MessageStream";
import { StatusPill } from "./StatusPill";

export function OverlayPanel() {
  const sessionId = useSessionStore((s) => s.sessionId);
  const status = useSessionStore((s) => s.status);
  const messages = useSessionStore((s) => s.messages);
  const streamingContent = useSessionStore((s) => s.streamingContent);
  const error = useSessionStore((s) => s.error);
  const addUserMessage = useSessionStore((s) => s.addUserMessage);

  const { sendQuery, sendClear } = useAetherWS({ sessionId });

  const isBusy = status === "thinking" || status === "connecting";
  const isDisconnected = status === "disconnected";

  const handleSend = (content: string) => {
    addUserMessage(content);
    sendQuery(content);
  };

  return (
    <div className="flex h-full w-full flex-col overflow-hidden rounded-2xl border border-zinc-700/60 bg-zinc-950/95 shadow-2xl backdrop-blur-xl">
      {/* Title bar / drag region */}
      <div
        data-tauri-drag-region
        className="flex items-center justify-between border-b border-zinc-700/50 px-4 py-3"
      >
        <div className="flex items-center gap-2">
          <span className="text-sm font-semibold text-zinc-200">Aether</span>
          <StatusPill status={status} />
        </div>
        <button
          onClick={sendClear}
          className="rounded-md px-2 py-1 text-xs text-zinc-500 transition hover:bg-zinc-800 hover:text-zinc-300"
          title="Clear conversation"
        >
          Clear
        </button>
      </div>

      {error && (
        <div className="mx-4 mt-2 rounded-lg bg-red-900/40 px-3 py-2 text-xs text-red-300">
          {error}
          {isDisconnected && " — make sure backend is running on :8787"}
        </div>
      )}

      <MessageStream messages={messages} streamingContent={streamingContent} />

      <ChatInput onSend={handleSend} disabled={isBusy || isDisconnected} />
    </div>
  );
}
