import { expect, test } from "@playwright/test";

test("live message delivery scenario", async ({ page }) => {
  await page.setContent("<main><div data-testid='message'>hello</div></main>");
  await expect(page.getByTestId("message")).toHaveText("hello");
});
