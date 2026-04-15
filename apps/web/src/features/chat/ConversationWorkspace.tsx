import React, { useCallback } from "react";

import type { ChatServerEvent } from "@chat-system/shared-types";

import MessageComposer from "./MessageComposer";
import MessageHistoryPanel from "./MessageHistoryPanel";
import ParticipantPresenceStrip from "./ParticipantPresenceStrip";
import { useLiveConversation } from "./useLiveConversation";
import { useMessageHistory } from "./useMessageHistory";
import { useParticipantPresence } from "./useParticipantPresence";

export interface ConversationWorkspaceProps {
  conversationId: string;
  userId: string;
  apiBaseUrl: string;
  websocketUrl: string;
}

export function ConversationWorkspace({
  conversationId,
  userId,
  apiBaseUrl,
  websocketUrl,
}: ConversationWorkspaceProps) {
  const { messages, setMessages, loadOlder } = useMessageHistory(apiBaseUrl, conversationId, userId);
  const { entries, applyPresenceEvent, rehydratePresenceState } = useParticipantPresence(
    apiBaseUrl,
    conversationId,
    userId,
  );
  const onEvent = useCallback(
    (event: ChatServerEvent) => {
      if (event.type === "message_created") {
        setMessages((currentMessages) => [...currentMessages, event.message]);
      }
      if (event.type === "history_synced") {
        setMessages(event.messages);
      }
      if (event.type === "presence_updated") {
        applyPresenceEvent(event);
      }
      if (event.type === "history_synced") {
        void rehydratePresenceState();
      }
    },
    [applyPresenceEvent, rehydratePresenceState, setMessages],
  );
  const { sendMessage } = useLiveConversation(websocketUrl, userId, conversationId, onEvent);

  return (
    <section aria-label="Conversation workspace">
      <header>
        <h1>Conversation</h1>
        <p>{conversationId}</p>
      </header>
      <main>
        <ParticipantPresenceStrip entries={entries} />
        <MessageHistoryPanel messages={messages} onLoadOlder={() => void loadOlder()} />
        <MessageComposer onSend={sendMessage} />
      </main>
    </section>
  );
}

export default ConversationWorkspace;