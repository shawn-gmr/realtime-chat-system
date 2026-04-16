import React, { useMemo, useState } from "react";

import ConversationWorkspace from "./features/chat/ConversationWorkspace";

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";
const websocketBaseUrl = import.meta.env.VITE_WEBSOCKET_URL ?? "ws://127.0.0.1:8000";

const demoConversationId = "11111111-1111-1111-1111-111111111111";
const demoUsers = {
  alice: "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
  bob: "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
} as const;

type DemoUserKey = keyof typeof demoUsers;

export default function App() {
  const [activeUser, setActiveUser] = useState<DemoUserKey>("alice");

  const websocketUrl = useMemo(
    () => `${websocketBaseUrl}/ws/conversations/${demoConversationId}?user_id=${demoUsers[activeUser]}`,
    [activeUser],
  );

  return (
    <div className="app-shell">
      <aside className="app-sidebar">
        <p className="eyebrow">Manual Test Harness</p>
        <h1>chat-system</h1>
        <p>
          Open this app in two browser tabs and switch one tab to Alice and the other to Bob.
          Messages and presence should update live across both tabs.
        </p>

        <label className="field">
          Active user
          <select
            value={activeUser}
            onChange={(event) => setActiveUser(event.target.value as DemoUserKey)}
          >
            <option value="alice">Alice</option>
            <option value="bob">Bob</option>
          </select>
        </label>

        <dl className="meta-list">
          <div>
            <dt>Conversation</dt>
            <dd>{demoConversationId}</dd>
          </div>
          <div>
            <dt>User id</dt>
            <dd>{demoUsers[activeUser]}</dd>
          </div>
          <div>
            <dt>API</dt>
            <dd>{apiBaseUrl}</dd>
          </div>
        </dl>
      </aside>

      <main className="app-main">
        <ConversationWorkspace
          conversationId={demoConversationId}
          userId={demoUsers[activeUser]}
          apiBaseUrl={apiBaseUrl}
          websocketUrl={websocketUrl}
        />
      </main>
    </div>
  );
}