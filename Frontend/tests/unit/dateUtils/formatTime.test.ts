import { describe, it, expect } from "vitest";
import { formatTime } from "../../../src/utils/dateUtils";

function getExpectedTime(date: Date | string): string {
  const d = new Date(date);
  return d.toLocaleTimeString(undefined, {
    hour: "numeric",
    minute: "numeric",
  });
}

describe("dateUtils:formatTime", () => {
  it("should format time correctly", () => {
    const date = new Date("2023-10-01T12:00:00Z");
    const expectedTime = getExpectedTime(date);
    const formattedTime = formatTime(date);
    expect(formattedTime).toBe(expectedTime);
  });

  it("should format a date string correctly", () => {
    const dateString = "2023-10-01T12:00:00Z";
    const expectedTime = getExpectedTime(dateString);
    const formattedTime = formatTime(dateString);
    expect(formattedTime).toBe(expectedTime);
  });

  it("should handle invalid date gracefully", () => {
    const invalidDate = "invalid-date-string";
    const formattedTime = formatTime(invalidDate);
    expect(formattedTime).toBe("Invalid time");
  });
});
