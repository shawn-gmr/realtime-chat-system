import React from "react";
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import ParticipantPresenceStrip from "../../src/features/chat/ParticipantPresenceStrip";

describe("ParticipantPresenceStrip", () => {
  it("renders participant statuses", () => {
    render(
      <ParticipantPresenceStrip
        entries={[{ user_id: "user-1", status: "online", last_activity_at: "2026-04-15T00:00:00Z" }]}
      />,
    );

    expect(screen.getByText("online")).toBeTruthy();
  });
});
