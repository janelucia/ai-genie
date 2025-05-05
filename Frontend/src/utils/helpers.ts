export const stringToArray = (input: string | undefined): string[] =>
  input ? input.split(",").map((i) => i.trim()) : [];

export function isUserSignedUp(eventId: string): boolean {
  const signedUpEvents = JSON.parse(
    localStorage.getItem("signed-up-events") || "[]",
  ) as { [key: string]: boolean }[];
  return signedUpEvents.some((event) => Object.keys(event)[0] === eventId);
}

export function signUpForEvent(eventId: string): void {
  const signedUpEvents = JSON.parse(
    localStorage.getItem("signed-up-events") || "[]",
  ) as { [key: string]: boolean }[];
  signedUpEvents.push({ [eventId]: true });
  localStorage.setItem("signed-up-events", JSON.stringify(signedUpEvents));
}
