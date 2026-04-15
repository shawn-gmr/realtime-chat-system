import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "jsdom",
    include: ["tests/component/**/*.test.ts?(x)"],
    exclude: ["tests/e2e/**", "test-results/**", "node_modules/**"],
  },
});
