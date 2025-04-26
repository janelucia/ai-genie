export const keywordsStringToArray = (
  keywords: string | undefined,
): string[] =>
  keywords ? keywords.split(",").map((keyword) => keyword.trim()) : [];

export function alreadySignedUp(id: string | undefined) {
  if (!id) return false;
  return !!localStorage.getItem(`signed-up-${id}`);
}
