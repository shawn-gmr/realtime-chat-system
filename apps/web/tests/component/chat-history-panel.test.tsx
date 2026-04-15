import React from "react";
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import MessageHistoryPanel from "../../src/features/chat/MessageHistoryPanel";

describe("MessageHistoryPanel", () => {
  it("renders the empty state", () => {
    render(<MessageHistoryPanel messages={[]} />);
    expect(screen.getByText("No messages yet.")).toBeTruthy();
  });
});
