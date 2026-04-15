import type { PresenceEntry } from "@chat-system/shared-types";

export async function fetchConversationPresence(
  apiBaseUrl: string,
  conversationId: string,
  userId: string,
) {
  const response = await fetch(
    `${apiBaseUrl}/api/conversations/${conversationId}/presence`,
    {
      headers: { "X-User-Id": userId },
    },
  );
  const payload = (await response.json()) as {
    conversation_id: string;
    participants: PresenceEntry[];
  };
  return payload.participants;
}
