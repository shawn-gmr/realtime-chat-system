import { useEffect, useState } from "react";

import type {
  PresenceEntry,
  PresenceUpdatedEvent,
} from "@chat-system/shared-types";

import { fetchConversationPresence } from "../../services/chatPresenceClient";

export function useParticipantPresence(
  apiBaseUrl: string,
  conversationId: string,
  userId: string,
) {
  const [entries, setEntries] = useState<PresenceEntry[]>([]);

  useEffect(() => {
    void fetchConversationPresence(apiBaseUrl, conversationId, userId).then(
      setEntries,
    );
  }, [apiBaseUrl, conversationId, userId]);

  const applyPresenceEvent = (event: PresenceUpdatedEvent) => {
    setEntries((currentEntries) => {
      const nextEntries = currentEntries.filter(
        (entry) => entry.user_id !== event.user_id,
      );
      nextEntries.push({
        user_id: event.user_id,
        status: event.status,
        last_activity_at: event.last_activity_at,
        scope: event.scope,
      });
      return nextEntries;
    });
  };

  const rehydratePresenceState = async () => {
    setEntries(
      await fetchConversationPresence(apiBaseUrl, conversationId, userId),
    );
  };

  return { entries, applyPresenceEvent, rehydratePresenceState };
}
