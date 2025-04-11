<template>
  <Header no-chat />
  <div
    class="pt-24 flex flex-col w-full max-w-md mx-auto gap-[var(--spacing-between-sections)]"
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
        {{ msg.ai_response ? "AI" : "You" }}
      </Text>
    </div>
  </div>
  <div class="flex w-full gap-2 fixed bottom-14 left-0 p-4 bg-base-100">
    <input
      v-model="input"
      class="input input-bordered w-full"
      placeholder="Type your message..."
      @keyup.enter="sendMessage"
    />
    <button class="btn btn-primary" @click="sendMessage">Send</button>
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import type { Chat, Message } from "../types/types.ts";
import Text from "../components/Text.vue";
import Header from "../components/Header.vue";
import { formatDate, formatTime } from "../utils/dateUtils.ts";
import { useApiFetch } from "../api/useApiFetch.ts";

const input = ref("");
const result = ref<Chat | null>(null);
const messages = ref<Message[]>([]);

const LOCAL_STORAGE_KEY = "chat-id";

const sendMessage = async () => {
  const content = input.value.trim();
  if (!content) return;

  const chatId = localStorage.getItem(LOCAL_STORAGE_KEY);
  if (!chatId) return;

  const userMessage: Message = {
    content,
    ai_response: false,
  };

  messages.value.push(userMessage);
  input.value = "";

  const resp = await fetch(`http://localhost:8000/api/message-ai/${chatId}/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      content: userMessage.content,
      ai_response: userMessage.ai_response,
    }),
  });

  const data = await resp.json();

  console.log(data);
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
