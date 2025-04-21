import { ref, type Ref } from "vue";

export function useApiFetch<T = unknown>(endpoint: string) {
  const data: Ref<T | null> = ref(null);
  const error: Ref<string | null> = ref(null);
  const loading = ref(true);

  const fetchData = async () => {
    loading.value = true;
    try {
      const response = await fetch(`http://localhost:8000/api/${endpoint}/`);
      if (!response.ok) throw new Error("Network response was not ok");
      data.value = await response.json();
    } catch (err: any) {
      error.value = err.message || "Unknown error";
    } finally {
      loading.value = false;
    }
  };

  // Auto-fetch immediately
  fetchData();

  return { data, error, loading };
}
