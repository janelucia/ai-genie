import { describe, it, expect } from "vitest";
import { formatDate } from "../../../src/utils/dateUtils";

function getExpectedDate(date: Date | string): string {
  const d = new Date(date);
  return d.toLocaleDateString(undefined, {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

describe("dateUtils:formatDate", () => {
  it("should format a date correctly", () => {
    const date = new Date("2023-10-01T12:00:00Z");
    const expectedDate = getExpectedDate(date);
    const formattedDate = formatDate(date);
    expect(formattedDate).toBe(expectedDate);
  });

  it("should format a date string correctly", () => {
    const dateString = "2023-10-01T12:00:00Z";
    const expectedDate = getExpectedDate(dateString);
    const formattedDate = formatDate(dateString);
    expect(formattedDate).toBe(expectedDate);
  });

  it("should handle invalid date gracefully", () => {
    const invalidDate = "invalid-date-string";
    const formattedDate = formatDate(invalidDate);
    expect(formattedDate).toBe("Invalid date");
  });
});
