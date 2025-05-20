/**
 * Formats a string to an array of strings. The backend returns a string with the keywords separated by commas.
 * To iterate over the different keywords, we need to convert the string to an array.
 * @param input
 */
export const stringToArray = (input: string | undefined): string[] =>
  input ? input.split(",").map((i) => i.trim()) : [];

/**
 * Checks if the user is signed up for an event by checking the local storage for the event ID.
 * - Event id can be found in the local storage under the key "signed-up-events".
 * - the event is an array of objects, where the key is the event ID and the value is a boolean.
 * @param eventId
 */
export function isUserSignedUp(eventId: string): boolean {
  const signedUpEvents = JSON.parse(
    localStorage.getItem("signed-up-events") || "[]",
  ) as { [key: string]: boolean }[];
  return signedUpEvents.some((event) => Object.keys(event)[0] === eventId);
}

/**
 * Signs up the user for an event by adding the event ID to the array if "signed-up-events" in local storage.
 */
export function signUpForEvent(eventId: string): void {
  const signedUpEvents = JSON.parse(
    localStorage.getItem("signed-up-events") || "[]",
  ) as { [key: string]: boolean }[];

  // Check if the user is already signed up for the event
  if (signedUpEvents.some((event) => Object.keys(event)[0] === eventId)) {
    return;
  }

  signedUpEvents.push({ [eventId]: true });
  localStorage.setItem("signed-up-events", JSON.stringify(signedUpEvents));
}
