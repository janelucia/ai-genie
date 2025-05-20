import { describe, it, expect, beforeEach } from "vitest";
import { signUpForEvent } from "../../../src/utils/helpers";

describe("signupForEvents", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it("should add the event to localStorage if not already signed up", () => {
    const eventId = "event-123";
    const mockData = JSON.stringify([{ "event-456": true }]);
    localStorage.setItem("signed-up-events", mockData);

    signUpForEvent(eventId);

    const signedUpEvents = JSON.parse(
      localStorage.getItem("signed-up-events") || "[]",
    );
    expect(signedUpEvents).toEqual([
      { "event-456": true },
      { [eventId]: true },
    ]);
  });

  it("should not add the event to localStorage if already signed up", () => {
    const eventId = "event-123";
    const mockData = JSON.stringify([{ [eventId]: true }]);
    localStorage.setItem("signed-up-events", mockData);

    signUpForEvent(eventId);

    const signedUpEvents = JSON.parse(
      localStorage.getItem("signed-up-events") || "[]",
    );
    expect(signedUpEvents).toEqual([{ [eventId]: true }]);
  });
});
