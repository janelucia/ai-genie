<template>
  <Header chat />
  <div
    class="overflow-y-auto max-h-[90vh] py-14 flex flex-col gap-[var(--spacing-in-sections)]"
  >
    <div class="w-full flex justify-center">
      <template v-if="isLoading">
        <video autoplay loop src="/video/talking-pepper.mp4" class="w-1/2" />
      </template>
      <template v-else>
        <video autoplay loop src="/video/blinking-pepper.mp4" class="w-1/2" />
      </template>
    </div>
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
        {{ msg.ai_response ? "AIGenie" : "You" }} -
        {{
          msg.created
            ? `${formatDate(msg.created)} ${formatTime(msg.created)}`
            : "Unknown time"
        }}
      </Text>
    </div>
    <div v-if="isLoading" class="self-start text-sm text-gray-500">
      AIGenie is typing…
    </div>
    <div id="bottomRef" class="h-14"></div>
  </div>
  <div class="flex w-full gap-2 fixed bottom-14 left-0 p-4 bg-base-100">
    <input
      v-model="input"
      ref="inputField"
      class="input input-bordered w-full"
      placeholder="Type your message..."
      @keyup.enter="sendMessage"
      @input="focusInput"
    />
    <button class="btn btn-secondary" @click="sendMessage">Send</button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, nextTick, onUnmounted } from "vue";
import type { Chat, Message } from "../types/types.ts";
import Text from "../components/Text.vue";
import Header from "../components/Header.vue";
import { formatDate, formatTime } from "../utils/dateUtils.ts";
import { $fetch } from "../api/useApiRequest.ts";

const LOCAL_STORAGE_KEY = "chat-id";
const chatId = ref(localStorage.getItem(LOCAL_STORAGE_KEY));

const messages = ref<Message[]>([]);
const isLoading = ref(false);
const input = ref("");
const inputField = ref<HTMLInputElement | null>(null);

/**
 * Focuses the input field when the user starts typing.
 */
const focusInput = () => {
  if (inputField.value && document.activeElement !== inputField.value) {
    inputField.value.focus();
  }
};

/**
 * Scrolls to the bottom of the chat window. This ensures that the user always sees the latest message.
 * @param behavior - The scroll behavior (default is "smooth").
 */
const scrollToBottom = async (behavior: ScrollBehavior = "smooth") => {
  await nextTick();
  const bottomRef = document.getElementById("bottomRef");
  if (bottomRef) {
    bottomRef.scrollIntoView({ behavior });
  }
};

/**
 * Sends a message and updates the chat window.
 * This function is called when the user presses Enter or clicks the Send button.
 */
const sendMessage = async () => {
  const content = input.value.trim();
  if (!content) return;

  const userMessage: Message = {
    content,
    ai_response: false,
    created: new Date(),
  };

  isLoading.value = true;

  messages.value.push(userMessage);
  input.value = "";

  const data = await $fetch<Message>(
    `message-ai/${chatId.value}/`,
    "POST",
    userMessage,
  );

  console.log(data.content);

  if (data.content) {
    isLoading.value = false;
    messages.value.push(data);
  } else {
    isLoading.value = false;
    messages.value.push({
      content: "Error sending message. Please try again.",
      ai_response: true,
      created: new Date(),
    });
  }
};

onMounted(async () => {
  if (!chatId.value) {
    const data = await $fetch<Chat>("chats/", "POST");
    if (data.id) {
      localStorage.setItem(LOCAL_STORAGE_KEY, data.id.toString());
      chatId.value = data.id.toString();
    }
  }

  const queuedMsg = localStorage.getItem("chat-message-research");
  if (queuedMsg) {
    input.value = queuedMsg;
    localStorage.removeItem("chat-message-research");
    await sendMessage();
  }
});

onUnmounted(() => {
  stop();
});

const isFirstLoad = ref(true);
watch(
  [messages],
  async () => {
    await scrollToBottom(isFirstLoad.value ? "instant" : "smooth");
    isFirstLoad.value = false;
  },
  { deep: true },
);
</script>
