/**
 * Formats a date into a human-readable string according to the user's locale.
 * @param date
 */
export function formatDate(date: Date | string): string {
  const d = new Date(date);
  if (isNaN(d.getTime())) {
    console.warn("Invalid date passed to formatDate:", date);
    return "Invalid date";
  }

  return d.toLocaleDateString(undefined, {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

/**
 * Formats a date into a human-readable time string according to the user's locale.
 * @param date
 */
export function formatTime(date: Date | string): string {
  const d = new Date(date);
  if (isNaN(d.getTime())) {
    console.warn("Invalid date passed to formatTime:", date);
    return "Invalid time";
  }

  return d.toLocaleTimeString(undefined, {
    hour: "numeric",
    minute: "numeric",
  });
}
