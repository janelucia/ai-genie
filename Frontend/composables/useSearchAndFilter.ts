import { ref, computed, type Ref } from "vue";

export default function useSearchAndFilter<T extends { keywords?: string }>(
  input: Ref<T[]>,
  getTextFields: (item: T) => string[],
) {
  const searchQuery = ref("");
  const selectedKeywords = ref<string[]>([]);

  const filteredResults = computed(() => {
    return input.value.filter((item) => {
      const query = searchQuery.value.toLowerCase();

      const keywordsArray = item.keywords
        ? item.keywords.split(",").map((k) => k.trim().toLowerCase())
        : [];

      const matchesTextFields = getTextFields(item).some((field) =>
        field.toLowerCase().includes(query),
      );

      const matchesKeywordSearch = keywordsArray.some((keyword) =>
        keyword.includes(query),
      );

      const matchesSelectedKeywords =
        selectedKeywords.value.length === 0 ||
        selectedKeywords.value.every((selected) =>
          keywordsArray.includes(selected.toLowerCase()),
        );

      return (
        (matchesTextFields || matchesKeywordSearch) && matchesSelectedKeywords
      );
    });
  });

  function applyKeywordFilter(keywords: string[]) {
    selectedKeywords.value = keywords;
  }

  return {
    searchQuery,
    filteredResults,
    applyKeywordFilter,
    selectedKeywords,
  };
}
