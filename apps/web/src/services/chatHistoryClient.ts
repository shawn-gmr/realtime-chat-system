import type { MessageHistoryResponse } from "@chat-system/shared-types";

export async function fetchConversationHistory(
  apiBaseUrl: string,
  conversationId: string,
  userId: string,
  beforeMessageId?: string | null,
) {
  const params = new URLSearchParams();
  if (beforeMessageId) {
    params.set("before_message_id", beforeMessageId);
  }
  const response = await fetch(
    `${apiBaseUrl}/api/conversations/${conversationId}/messages?${params.toString()}`,
    { headers: { "X-User-Id": userId } },
  );
  return (await response.json()) as MessageHistoryResponse;
}
