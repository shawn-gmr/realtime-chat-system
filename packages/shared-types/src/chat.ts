export type PresenceStatus = "online" | "away" | "offline";

export interface ChatMessage {
  id: string;
  conversation_id: string;
  sender_id: string;
  body: string;
  sent_at: string;
  sequence_number: number;
}

export interface PresenceEntry {
  user_id: string;
  status: PresenceStatus;
  last_activity_at: string;
  last_connected_at?: string | null;
  scope?: "global";
}

export interface MessageHistoryResponse {
  conversation_id: string;
  messages: ChatMessage[];
  has_more: boolean;
  next_before_message_id?: string | null;
}

export interface SendMessageCommand {
  type: "send_message";
  conversation_id: string;
  client_message_id: string;
  body: string;
}

export interface HeartbeatCommand {
  type: "heartbeat";
  conversation_id: string;
}

export interface ConnectCommand {
  type: "connect";
  conversation_id: string;
  last_seen_message_id?: string | null;
}

export interface HistorySyncedEvent {
  type: "history_synced";
  conversation_id: string;
  messages: ChatMessage[];
  replay_complete: boolean;
}

export interface MessageCreatedEvent {
  type: "message_created";
  conversation_id: string;
  message: ChatMessage;
}

export interface PresenceUpdatedEvent {
  type: "presence_updated";
  conversation_id: string;
  user_id: string;
  status: PresenceStatus;
  last_activity_at: string;
  scope: "global";
}

export interface MessageFailedEvent {
  type: "message_failed";
  conversation_id: string;
  client_message_id: string;
  code: string;
  message: string;
}

export type ChatServerEvent =
  | HistorySyncedEvent
  | MessageCreatedEvent
  | PresenceUpdatedEvent
  | MessageFailedEvent;

export type ChatClientCommand =
  | ConnectCommand
  | SendMessageCommand
  | HeartbeatCommand;
