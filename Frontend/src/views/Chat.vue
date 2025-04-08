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
          msg.sender === 'you'
            ? 'bg-primary text-primary-content self-end'
            : 'bg-base-300 self-start',
        ]"
      >
        <Text>
          {{ msg.text }}
        </Text>
      </div>
      <Text :class="msg.sender === 'you' ? 'self-end' : 'self-start'" small
        >{{ msg.sender }} - {{ formatDate(msg.timestamp) }},
        {{ formatTime(msg.timestamp) }}
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
import type { ChatMessage } from "../types/types.ts";
import Text from "../components/Text.vue";
import Header from "../components/Header.vue";
import { formatDate, formatTime } from "../utils/dateUtils.ts";

const messages = ref<ChatMessage[]>([]);
const input = ref("");

const LOCAL_STORAGE_KEY = "my-chat-history";

function sendMessage() {
  if (!input.value.trim()) return;

  const userMessage: ChatMessage = {
    text: input.value,
    sender: "you",
    timestamp: new Date().toISOString(),
  };

  messages.value.push(userMessage);

  // Bot response simulation
  setTimeout(() => {
    messages.value.push({
      text: `Echo: ${input.value}`,
      sender: "bot",
      timestamp: new Date().toISOString(),
    });
  }, 500);

  input.value = "";
}

watch(
  messages,
  () => {
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(messages.value));
  },
  { deep: true },
);

onMounted(() => {
  const saved = localStorage.getItem(LOCAL_STORAGE_KEY);
  if (saved) {
    messages.value = JSON.parse(saved);
  }
});
</script>
