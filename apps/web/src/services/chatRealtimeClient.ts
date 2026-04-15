import type {
  ChatClientCommand,
  ChatServerEvent,
} from "@chat-system/shared-types";

export class ChatRealtimeClient {
  private socket: WebSocket | null = null;

  constructor(
    private readonly url: string,
    private readonly userId: string,
    private readonly onEvent: (event: ChatServerEvent) => void,
  ) {}

  connect(initialCommand: ChatClientCommand) {
    if (typeof WebSocket === "undefined") {
      return;
    }
    this.socket = new WebSocket(this.url);
    this.socket.addEventListener("open", () => {
      this.socket?.send(JSON.stringify(initialCommand));
    });
    this.socket.addEventListener("message", (event) => {
      this.onEvent(JSON.parse(event.data) as ChatServerEvent);
    });
  }

  send(command: ChatClientCommand) {
    this.socket?.send(JSON.stringify(command));
  }

  dispose() {
    this.socket?.close();
    this.socket = null;
  }

  headers() {
    return { "X-User-Id": this.userId };
  }
}
