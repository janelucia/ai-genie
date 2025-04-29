export function formatDate(date: Date): string {
  const d = new Date(date);
  if (isNaN(d.getTime())) {
    console.warn("Invalid date passed to formatDate:", date);
    return "Invalid date";
  }

  return new Intl.DateTimeFormat("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  }).format(d);
}

export function formatTime(date: Date): string {
  const d = new Date(date);
  if (isNaN(d.getTime())) {
    console.warn("Invalid date passed to formatTime:", date);
    return "Invalid time";
  }

  return new Intl.DateTimeFormat("en-US", {
    hour: "numeric",
    minute: "numeric",
  }).format(d);
}
