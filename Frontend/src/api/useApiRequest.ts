import { ref, type Ref } from "vue";

export function useApiRequest<T = unknown>(
  endpoint: string,
  method: "GET" | "POST" | "PUT" | "DELETE" = "GET",
  bodyData?: unknown,
) {
  const baseUrl =
    import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/";
  const data: Ref<T | null> = ref(null);
  const error: Ref<string | null> = ref(null);
  const loading = ref(false);
  console.log(baseUrl);

  const execute = async () => {
    loading.value = true;
    try {
      const options: RequestInit = {
        method,
        headers: {
          "Content-Type": "application/json",
          "ngrok-skip-browser-warning": "true",
        },
      };

      if (bodyData) {
        options.body = JSON.stringify(bodyData);
      }

      const response = await fetch(baseUrl + endpoint, options);

      if (!response.ok)
        throw new Error(`Error ${response.status}: ${response.statusText}`);
      data.value = await response.json();
    } catch (err: any) {
      error.value = err.message || "Unknown error";
    } finally {
      loading.value = false;
    }
  };

  console.log(endpoint, method, bodyData);

  if (method === "GET") execute();

  return { data, error, loading, execute };
}
