import React from "react";
import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import MessageComposer from "../../src/features/chat/MessageComposer";

describe("MessageComposer", () => {
  it("submits the typed message", async () => {
    const onSend = vi.fn();
    render(<MessageComposer onSend={onSend} />);

    fireEvent.change(screen.getByLabelText("Message"), { target: { value: "hello" } });
    fireEvent.click(screen.getByText("Send"));

    expect(onSend).toHaveBeenCalledWith("hello");
  });
});
