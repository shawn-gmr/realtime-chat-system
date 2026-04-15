import React from "react";

import type { ChatMessage } from "@chat-system/shared-types";

export interface MessageHistoryPanelProps {
  messages: ChatMessage[];
  onLoadOlder?: () => void;
}

export function MessageHistoryPanel({ messages, onLoadOlder }: MessageHistoryPanelProps) {
  if (messages.length === 0) {
    return <div>No messages yet.</div>;
  }

  return (
    <section>
      <button type="button" onClick={onLoadOlder}>
        Load older
      </button>
      <ul>
        {messages.map((message) => (
          <li key={message.id}>
            <strong>{message.sender_id}</strong>
            <span>{message.body}</span>
          </li>
        ))}
      </ul>
    </section>
  );
}

export default MessageHistoryPanel;
