import { $fetch } from "./useApiRequest.ts";
import type { ChatWithMessages } from "../types/types.ts";
import { type Ref, ref } from "vue";

/**
 * Loads the chat messages from the server and updates the chat window.
 * @param chatId
 */
export const useChatAPI = (chatId: Ref<string | null>) => {
  const messages = ref<ChatWithMessages["messages"]>([]);
  const isLoading = ref(false);

  const updateChat = async () => {
    if (!chatId.value) return;
    try {
      const data = await $fetch<ChatWithMessages>(
        "chats/" + chatId.value,
        "GET",
      );
      if (isLoading.value) {
        isLoading.value = data.messages.length <= messages.value.length;
      }
      messages.value = data.messages;
    } catch (err) {
      console.error("Chat API error:", err);
      isLoading.value = false;
    }
  };

  void updateChat();

  const interval = setInterval(() => {
    void updateChat();
  }, 1000);

  return { stop: () => clearInterval(interval), messages, isLoading };
};
