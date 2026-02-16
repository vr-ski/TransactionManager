import { test, expect } from "@playwright/test";

test("user can log in and sees transactions page", async ({ page }) => {
  // Go to the login page (assuming frontend runs on port 5173)
  await page.goto("http://localhost:5173");

  // Fill login form
  await page.fill("#username", "client");
  await page.fill("#password", "s3cre7P@ssW0rD!");
  await page.click('button[type="submit"]');

  // Wait for navigation and verify the transactions header appears
  await expect(page.locator("h2.section-header")).toHaveText(
    "Recent Transactions",
  );

  // Optionally check that token is stored
  const token = await page.evaluate(() => localStorage.getItem("access_token"));
  expect(token).toBeTruthy();
});
