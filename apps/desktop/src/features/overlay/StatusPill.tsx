import type { SessionStatus } from "../../shared/types";

const STATUS_CONFIG: Record<
  SessionStatus,
  { label: string; color: string; dot: string }
> = {
  idle: { label: "Ready", color: "text-zinc-400", dot: "bg-zinc-500" },
  connecting: { label: "Connecting", color: "text-yellow-400", dot: "bg-yellow-400 animate-pulse" },
  disconnected: { label: "Disconnected", color: "text-red-400", dot: "bg-red-400" },
  listening: { label: "Listening", color: "text-blue-400", dot: "bg-blue-400 animate-pulse" },
  watching: { label: "Watching", color: "text-cyan-400", dot: "bg-cyan-400 animate-pulse" },
  thinking: { label: "Thinking", color: "text-purple-400", dot: "bg-purple-400 animate-pulse" },
  researching: { label: "Researching", color: "text-indigo-400", dot: "bg-indigo-400 animate-pulse" },
  executing: { label: "Executing", color: "text-orange-400", dot: "bg-orange-400 animate-pulse" },
  done: { label: "Done", color: "text-green-400", dot: "bg-green-400" },
  error: { label: "Error", color: "text-red-400", dot: "bg-red-400" },
};

interface StatusPillProps {
  status: SessionStatus;
}

export function StatusPill({ status }: StatusPillProps) {
  const config = STATUS_CONFIG[status] ?? STATUS_CONFIG.idle;

  return (
    <div className="flex items-center gap-2 rounded-full bg-zinc-800/80 px-3 py-1 text-xs font-medium">
      <span className={`h-2 w-2 rounded-full ${config.dot}`} />
      <span className={config.color}>{config.label}</span>
    </div>
  );
}
