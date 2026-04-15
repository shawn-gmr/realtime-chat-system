import React, { useState } from "react";

export interface MessageComposerProps {
  onSend: (body: string) => Promise<void> | void;
}

export function MessageComposer({ onSend }: MessageComposerProps) {
  const [body, setBody] = useState("");

  return (
    <form
      onSubmit={async (event) => {
        event.preventDefault();
        if (!body.trim()) {
          return;
        }
        await onSend(body);
        setBody("");
      }}
    >
      <label>
        Message
        <textarea value={body} onChange={(event) => setBody(event.target.value)} />
      </label>
      <button type="submit">Send</button>
    </form>
  );
}

export default MessageComposer;
