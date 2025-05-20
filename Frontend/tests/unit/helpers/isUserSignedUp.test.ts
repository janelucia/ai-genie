// isUserSignedUp.test.ts
import { describe, it, expect, afterEach } from "vitest";
import { isUserSignedUp } from "../../../src/utils/helpers";

describe("isUserSignedUp", () => {
  afterEach(() => {
    localStorage.clear();
  });

  it("returns true if the user is signed up for the event", () => {
    const mockData = JSON.stringify([{ "event-123": true }]);
    localStorage.setItem("signed-up-events", mockData);

    const result = isUserSignedUp("event-123");
    expect(result).toBe(true);
  });

  it("returns false if the user is not signed up for the event", () => {
    const mockData = JSON.stringify([{ "event-456": true }]);
    localStorage.setItem("signed-up-events", mockData);

    const result = isUserSignedUp("event-123");
    expect(result).toBe(false);
  });

  it("returns false if signed-up-events is missing", () => {
    localStorage.removeItem("signed-up-events");

    const result = isUserSignedUp("event-123");
    expect(result).toBe(false);
  });
});
