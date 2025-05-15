import { ref, type Ref } from "vue";

/**
 * A composable function to make API requests using the FETCH API from JavaScript.
 * Supports GET, POST, PUT, and DELETE methods.
 *
 * @param endpoint - The API endpoint to call (e.g., "chats/", "research/", "events/", "researchers/", "email/")
 * @param method - HTTP method to use for the request (default is GET)
 * @param bodyData - optional data to be sent in the request body
 * @returns An object containing the response data, error message, loading state, and a function to execute the request
 */
export function useApiRequest<T = unknown>(
  endpoint: string,
  method: "GET" | "POST" | "PUT" | "DELETE" = "GET",
  bodyData?: unknown,
) {
  const baseUrl = import.meta.env.VITE_API_BASE_URL
    ? import.meta.env.VITE_API_BASE_URL + "/api/"
    : "http://localhost:8000/api/";
  const data: Ref<T | null> = ref(null);
  const error: Ref<string | null> = ref(null);
  const loading = ref(false);

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

  if (method === "GET") execute();

  return { data, error, loading, execute };
}
