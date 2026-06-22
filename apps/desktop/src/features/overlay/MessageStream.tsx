import { useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";

import type { ChatMessage } from "../../shared/types";

interface MessageStreamProps {
  messages: ChatMessage[];
  streamingContent: string;
}

export function MessageStream({ messages, streamingContent }: MessageStreamProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, streamingContent]);

  if (messages.length === 0 && !streamingContent) {
    return (
      <div className="flex flex-1 flex-col items-center justify-center gap-2 p-6 text-center">
        <p className="text-lg font-medium text-zinc-300">Aether Assistant</p>
        <p className="text-sm text-zinc-500">
          Local-first AI. Press Alt+Space to toggle. Ask anything.
        </p>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-3">
      {messages.map((msg) => (
        <div
          key={msg.id}
          className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
        >
          <div
            className={`max-w-[85%] rounded-xl px-3 py-2 text-sm ${
              msg.role === "user"
                ? "bg-purple-600/80 text-white"
                : "bg-zinc-800/90 text-zinc-100"
            }`}
          >
            {msg.role === "assistant" ? (
              <ReactMarkdown>{msg.content}</ReactMarkdown>
            ) : (
              msg.content
            )}
          </div>
        </div>
      ))}

      {streamingContent && (
        <div className="flex justify-start">
          <div className="max-w-[85%] rounded-xl bg-zinc-800/90 px-3 py-2 text-sm text-zinc-100">
            <ReactMarkdown>{streamingContent}</ReactMarkdown>
            <span className="ml-1 inline-block h-3 w-1 animate-pulse bg-purple-400" />
          </div>
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  );
}
