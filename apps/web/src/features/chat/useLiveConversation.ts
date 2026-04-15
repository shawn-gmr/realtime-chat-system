import { useEffect, useMemo } from "react";

import type { ChatMessage, ChatServerEvent } from "@chat-system/shared-types";

import { ChatRealtimeClient } from "../../services/chatRealtimeClient";

export function useLiveConversation(
  websocketUrl: string,
  userId: string,
  conversationId: string,
  onEvent: (event: ChatServerEvent) => void,
) {
  const client = useMemo(
    () => new ChatRealtimeClient(websocketUrl, userId, onEvent),
    [conversationId, onEvent, userId, websocketUrl],
  );

  useEffect(() => {
    client.connect({
      type: "connect",
      conversation_id: conversationId,
      last_seen_message_id: null,
    });
    return () => client.dispose();
  }, [client, conversationId]);

  const sendMessage = async (body: string) => {
    client.send({
      type: "send_message",
      conversation_id: conversationId,
      client_message_id: crypto.randomUUID(),
      body,
    });
  };

  const sendHeartbeat = () => {
    client.send({ type: "heartbeat", conversation_id: conversationId });
  };

  return { sendMessage, sendHeartbeat };
}
