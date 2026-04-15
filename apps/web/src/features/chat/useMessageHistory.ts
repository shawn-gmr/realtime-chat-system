import { useEffect, useState } from "react";

import type { ChatMessage } from "@chat-system/shared-types";

import { fetchConversationHistory } from "../../services/chatHistoryClient";

export function useMessageHistory(
  apiBaseUrl: string,
  conversationId: string,
  userId: string,
) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [nextBeforeMessageId, setNextBeforeMessageId] = useState<string | null>(
    null,
  );

  useEffect(() => {
    void fetchConversationHistory(apiBaseUrl, conversationId, userId).then(
      (payload) => {
        setMessages(payload.messages);
        setNextBeforeMessageId(payload.next_before_message_id ?? null);
      },
    );
  }, [apiBaseUrl, conversationId, userId]);

  const loadOlder = async () => {
    const payload = await fetchConversationHistory(
      apiBaseUrl,
      conversationId,
      userId,
      nextBeforeMessageId,
    );
    setMessages((currentMessages) => [...payload.messages, ...currentMessages]);
    setNextBeforeMessageId(payload.next_before_message_id ?? null);
  };

  return { messages, setMessages, loadOlder };
}
