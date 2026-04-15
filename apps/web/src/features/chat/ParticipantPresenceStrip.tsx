import React from "react";

import type { PresenceEntry } from "@chat-system/shared-types";

export interface ParticipantPresenceStripProps {
  entries: PresenceEntry[];
}

export function ParticipantPresenceStrip({ entries }: ParticipantPresenceStripProps) {
  return (
    <ul aria-label="Participant presence">
      {entries.map((entry) => (
        <li key={entry.user_id}>
          <span>{entry.user_id}</span>
          <span>{entry.status}</span>
        </li>
      ))}
    </ul>
  );
}

export default ParticipantPresenceStrip;
