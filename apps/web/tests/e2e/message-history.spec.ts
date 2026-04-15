import { expect, test } from "@playwright/test";

test("message history scenario", async ({ page }) => {
  await page.setContent("<main><button>Load older</button></main>");
  await expect(page.getByText("Load older")).toBeVisible();
});
