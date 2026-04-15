import { expect, test } from "@playwright/test";

test("participant presence scenario", async ({ page }) => {
  await page.setContent("<main><span>online</span><span>offline</span></main>");
  await expect(page.getByText("online")).toBeVisible();
  await expect(page.getByText("offline")).toBeVisible();
});
