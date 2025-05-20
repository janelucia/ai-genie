import { describe, it, expect, beforeEach } from "vitest";
import { ref } from "vue";
import useSearchAndFilter from "../../../composables/useSearchAndFilter";

type Item = {
  title: string;
  description: string;
  keywords?: string;
};

describe("useSearchAndFilter", () => {
  let items = ref<Item[]>([]);

  beforeEach(() => {
    items.value = [
      {
        title: "Vue 3 Composition API",
        description: "Learn about reactivity and composables",
        keywords: "vue,composition,reactivity",
      },
      {
        title: "Testing with Vitest",
        description: "How to test your Vue apps",
        keywords: "testing,vitest,vue",
      },
      {
        title: "No keywords item",
        description: "Edge case without keywords",
      },
    ];
  });

  const getTextFields = (item: Item) => [item.title, item.description];

  // Test cases for search queries
  it("filters by search query for title", () => {
    const { searchQuery, filteredResults } = useSearchAndFilter(
      items,
      getTextFields,
    );

    searchQuery.value = "No";

    expect(filteredResults.value.length).toBe(1);
    expect(filteredResults.value.map((i) => i.title)).toContain(
      "No keywords item",
    );
  });

  it("filters by search query for description", () => {
    const { searchQuery, filteredResults } = useSearchAndFilter(
      items,
      getTextFields,
    );

    searchQuery.value = "Edge";

    expect(filteredResults.value.length).toBe(1);
    expect(filteredResults.value.map((i) => i.title)).toContain(
      "No keywords item",
    );
  });

  it("filters by search query in keywords", () => {
    const { searchQuery, filteredResults } = useSearchAndFilter(
      items,
      getTextFields,
    );

    searchQuery.value = "reactivity";

    expect(filteredResults.value.length).toBe(1);
    expect(filteredResults.value[0].title).toBe("Vue 3 Composition API");
  });

  it("returns nothing if the search query doesn't match", () => {
    const { searchQuery, filteredResults } = useSearchAndFilter(
      items,
      getTextFields,
    );

    searchQuery.value = "nonexistent";

    expect(filteredResults.value.length).toBe(0);
  });

  // Test cases for keyword filtering
  it("filters by selected keywords", () => {
    const { applyKeywordFilter, filteredResults } = useSearchAndFilter(
      items,
      getTextFields,
    );

    applyKeywordFilter(["vue"]);

    expect(filteredResults.value.length).toBe(2);
    expect(filteredResults.value.map((i) => i.title)).toContain(
      "Vue 3 Composition API",
    );
    expect(filteredResults.value.map((i) => i.title)).toContain(
      "Testing with Vitest",
    );
  });

  it("filters by multiple selected keywords", () => {
    const { applyKeywordFilter, filteredResults } = useSearchAndFilter(
      items,
      getTextFields,
    );

    applyKeywordFilter(["vue", "testing"]);

    expect(filteredResults.value.length).toBe(1);
    expect(filteredResults.value.map((i) => i.title)).toContain(
      "Testing with Vitest",
    );
  });

  it("returns nothing if the keywords don't match", () => {
    const { applyKeywordFilter, filteredResults } = useSearchAndFilter(
      items,
      getTextFields,
    );

    applyKeywordFilter(["vitest", "reactivity"]);

    expect(filteredResults.value.length).toBe(0);
  });

  // Test cases for combined search query and keyword filtering
  it("combines search query and selected keywords", () => {
    const { searchQuery, applyKeywordFilter, filteredResults } =
      useSearchAndFilter(items, getTextFields);

    searchQuery.value = "composition";
    applyKeywordFilter(["vue"]);

    expect(filteredResults.value.length).toBe(1);
    expect(filteredResults.value[0].title).toBe("Vue 3 Composition API");
  });

  it("returns all items when query and keywords are empty", () => {
    const { filteredResults } = useSearchAndFilter(items, getTextFields);
    expect(filteredResults.value.length).toBe(3);
  });
});
