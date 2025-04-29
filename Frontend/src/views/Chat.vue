<template>
  <Header chat />
  <div
    class="overflow-y-auto max-h-[90vh] py-14 flex flex-col gap-[var(--spacing-in-sections)]"
  >
    <video
      id="blinkingPepper"
      autoplay
      loop
      src="../assets/video/blinking-pepper.mp4"
    />
    <div
      v-for="(msg, i) in messages"
      :key="i"
      class="w-full flex flex-col gap-2"
    >
      <div
        :class="[
          'p-2 rounded w-fit',
          msg.ai_response
            ? 'bg-neutral text-neutral-content self-start'
            : 'bg-secondary text-base-100 self-end',
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

const scrollToBottom = (behavior: ScrollBehavior = "smooth") => {
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

  await nextTick();
  scrollToBottom();

  await useChatAPI(chatId, userMessage);
};

const useChatAPI = async (chatId: string, userMessage: Message) => {
  try {
    isLoading.value = true;

    await fetch(`http://localhost:8000/api/message-ai/${chatId}/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userMessage),
    });

    const MAX_TRIES = 30;
    const DELAY_MS = 1000;
    let tries = 0;

    while (tries < MAX_TRIES) {
      const { data } = await useApiFetch<Chat>("chats/" + chatId);
      await new Promise((resolve) => setTimeout(resolve, DELAY_MS));
      tries++;

      if (
        data.value?.messages?.length &&
        data.value.messages.length > messages.value.length
      ) {
        messages.value = data.value.messages;
        return;
      }
    }

    console.warn("AI response timeout");
  } catch (err) {
    console.error("Chat API error:", err);
  } finally {
    isLoading.value = false;
  }
};

onMounted(async () => {
  const chatId = localStorage.getItem(LOCAL_STORAGE_KEY);
  messages.value = [];

  if (chatId) {
    const { data } = useApiFetch<Chat>("chats/" + chatId);

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

    const queuedMsg = localStorage.getItem("chat-message-research");
    if (queuedMsg) {
      const msg: Message = {
        content: queuedMsg,
        ai_response: false,
        created: new Date(),
      };
      messages.value.push(msg);
      localStorage.removeItem("chat-message-research");
      await useChatAPI(chatId, msg);
    }

    await nextTick();
    scrollToBottom("instant");
  } else {
    const res = await fetch("http://localhost:8000/api/chats/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    });
    const newChat = await res.json();
    result.value = newChat;

    if (newChat?.id) {
      localStorage.setItem(LOCAL_STORAGE_KEY, newChat.id);
    }
  }
});

watch(
  [messages, isLoading],
  async () => {
    await nextTick();
    scrollToBottom();
  },
  { deep: true },
);
</script>
