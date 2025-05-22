import { ref, type Ref } from "vue";

/**
 * Fetches data from the API.
 * @param endpoint
 * @param method
 * @param bodyData
 */
export async function $fetch<T>(
  endpoint: string,
  method: "GET" | "POST" | "PUT" | "DELETE",
  bodyData?: unknown,
): Promise<T> {
  const baseUrl = import.meta.env.VITE_API_BASE_URL
    ? import.meta.env.VITE_API_BASE_URL + "/api/"
    : "http://localhost:8000/api/";

  const options: RequestInit = {
    method,
    headers: {
      "Content-Type": "application/json",
    },
  };

  if (bodyData) {
    options.body = JSON.stringify(bodyData);
  }

  const response = await fetch(baseUrl + endpoint, options);

  if (!response.ok)
    throw new Error(`Error ${response.status}: ${response.statusText}`);
  return response.json();
}

/**
 * Fetches data (only GET) from the API and returns it reactively.
 * @param endpoint
 */
export function useApiData<T = unknown>(endpoint: string) {
  const data: Ref<T | null> = ref(null);
  const error: Ref<string | null> = ref(null);
  const loading = ref(false);

  const execute = async () => {
    loading.value = true;
    try {
      data.value = await $fetch<T>(endpoint, "GET");
    } catch (err: any) {
      error.value = err.message || "Unknown error";
    } finally {
      loading.value = false;
    }
  };

  void execute();

  return { data, error, loading, execute };
}
