export const keywordsStringToArray = (
  keywords: string | undefined,
): string[] =>
  keywords ? keywords.split(",").map((keyword) => keyword.trim()) : [];
