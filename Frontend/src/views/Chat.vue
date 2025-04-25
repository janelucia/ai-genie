<template>
  <Header chat />
  <div
    class="overflow-y-auto max-h-[90vh] pt-14 flex flex-col gap-[var(--spacing-in-sections)]"
  >
    <div
      v-for="(msg, i) in messages"
      :key="i"
      class="w-full flex flex-col gap-2"
    >
      <div
        :class="[
          'p-2 rounded w-fit',
          msg.ai_response
            ? 'bg-base-300 self-start'
            : 'bg-primary text-primary-content self-end',
        ]"
      >
        <Text>
          {{ msg.content }}
        </Text>
      </div>
      <Text :class="msg.ai_response ? 'self-start' : 'self-end'" small>
        {{ msg.ai_response ? "AI" : "You" }} - {{ formatDate(msg.created) }}
        {{ formatTime(msg.created) }}
      </Text>
    </div>
    <div v-if="isLoading" class="self-start text-sm text-gray-500">
      AI is typing…
    </div>
    <div id="bottomRef" class="h-14"></div>
  </div>
  <div class="flex w-full gap-2 fixed bottom-14 left-0 p-4 bg-base-100">
    <input
      v-model="input"
      class="input input-bordered w-full"
      placeholder="Type your message..."
      @keyup.enter="sendMessage"
    />
    <button class="btn btn-secondary" @click="sendMessage">Send</button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from "vue";
import type { Chat, Message } from "../types/types.ts";
import Text from "../components/Text.vue";
import Header from "../components/Header.vue";
import { formatDate, formatTime } from "../utils/dateUtils.ts";
import { useApiFetch } from "../api/useApiFetch.ts";

const input = ref("");
const result = ref<Chat | null>(null);
const messages = ref<Message[]>([]);

const LOCAL_STORAGE_KEY = "chat-id";

const isLoading = ref(false);

const scrollToBottom = (behavior: string) => {
  const bottomRef = document.getElementById("bottomRef");
  if (bottomRef) {
    bottomRef.scrollIntoView({ behavior });
  }
};

const sendMessage = async () => {
  const content = input.value.trim();
  if (!content) return;

  const chatId = localStorage.getItem(LOCAL_STORAGE_KEY);
  if (!chatId) return;

  const userMessage: Message = {
    content,
    ai_response: false,
    created: new Date(),
  };

  messages.value.push(userMessage);
  input.value = "";
  isLoading.value = true;

  await nextTick();
  scrollToBottom("smooth");

  try {
    await fetch(`http://localhost:8000/api/message-ai/${chatId}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(userMessage),
    });

    const waitForAIResponse = async () => {
      const MAX_TRIES = 30;
      const DELAY_MS = 1000;
      let tries = 0;

      while (tries < MAX_TRIES) {
        const { data } = useApiFetch<Chat>("chats/" + chatId);
        await new Promise((resolve) => setTimeout(resolve, DELAY_MS));
        tries++;

        if (data.value?.messages?.length > messages.value.length) {
          messages.value = data.value.messages;
          return;
        }
      }

      console.warn("AI response timeout");
    };

    await waitForAIResponse();
  } catch (err) {
    console.error("Error during message send or AI response wait:", err);
  } finally {
    isLoading.value = false;
    scrollToBottom("smooth");
  }
};

onMounted(async () => {
  const id = localStorage.getItem(LOCAL_STORAGE_KEY);
  messages.value = [];

  if (id) {
    const { data } = useApiFetch<Chat>("chats/" + id);

    const waitForData = () =>
      new Promise<void>((resolve) => {
        const interval = setInterval(() => {
          if (data.value) {
            clearInterval(interval);
            resolve();
          }
        }, 50);
      });

    await waitForData();

    if (data.value) {
      result.value = data.value;
      messages.value = data.value.messages;
    }

    await nextTick();
    scrollToBottom("instant");
  } else {
    const response = await fetch("http://localhost:8000/api/chats/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const data = await response.json();
    result.value = data;

    if (data?.id) {
      localStorage.setItem(LOCAL_STORAGE_KEY, data.id);
    }
  }
});

watch(
  () => result.value,
  async (chat) => {
    if (chat?.chat?.id) {
      const { data } = useApiFetch<Chat>("chats/" + chat.chat.id);

      if (data.value?.messages?.length > messages.value.length) {
        messages.value = data.value.messages;
      }
    }
  },
  { deep: true },
);
</script>
