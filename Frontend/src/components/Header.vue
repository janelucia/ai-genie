<template>
  <div
    class="flex w-full justify-between gap-[var(--spacing-in-sections)] items-center fixed bg-primary top-0 left-0 z-10 px-4 py-2 rounded-b-lg"
  >
    <template v-if="noBack">
      <div class="w-8"></div>
    </template>
    <template v-else>
      <img
        src="/icons/arrow-back.svg"
        alt="Back"
        class="w-8 h-8 cursor-pointer"
        @click="router.go(-1)"
      />
    </template>

    <div class="flex-grow flex items-center justify-center">
      <img src="/icons/logo.svg" alt="Logo" class="cursor-pointer h-10" />
    </div>

    <template v-if="chat">
      <button @click="openModal">
        <img src="/icons/trash-can.svg" alt="Delete icon" />
      </button>
    </template>
    <template v-else>
      <div class="w-8"></div>
    </template>

    <dialog ref="modal" id="delete-confirmation-modal" class="modal">
      <div class="modal-box">
        <h3 class="font-bold text-lg">Delete Chat</h3>
        <p class="py-4">
          Deleting this chat will erase your previous messages and start a new
          session. Are you sure you want to continue?
        </p>
        <div class="modal-action">
          <button class="btn btn-error" @click="deleteChat">Delete</button>
          <form method="dialog">
            <button class="btn">Close</button>
          </form>
        </div>
      </div>
    </dialog>

    <Alert
      v-if="showToast"
      class="toast toast-top toast-end"
      :alert-type="alertType"
    >
      <Text>
        {{ toastMessage }}
      </Text>
    </Alert>
  </div>
</template>
<script setup lang="ts">
import router from "../router";
import { onMounted, ref } from "vue";
import { useApiRequest } from "../api/useApiRequest.ts";
import type { AlertType, ChatWithMessages } from "../types/types.ts";
import Alert from "./Alert.vue";
import Text from "./Text.vue";

defineProps<{
  chat?: boolean;
  noBack?: boolean;
}>();

const modal = ref<HTMLDialogElement | null>(null);
const toastMessage = ref("");
const toastClass = ref("");
const showToast = ref(false);
const alertType = ref<AlertType>("info");

/**
 * Deletes the chat by sending a DELETE request to the API.
 * - If the chat ID is not found, it shows an error message and reloads the page, to fetch a new chat id.
 * - If the chat has no messages, it shows a error message, that there are no messages to delete. There is no reload and the chat id is not replaced to prevent an increase in distributing unnecessary chat ids.
 * - If the chat is deleted successfully, it shows a success message and reloads the page.
 */
const deleteChat = async () => {
  const chatId = localStorage.getItem("chat-id");

  try {
    if (!chatId) {
      modal.value?.close();
      localStorage.setItem("toast-message", "No chat ID found.");
      localStorage.setItem("toast-class", "alert-error");
      localStorage.setItem("toast-should-show", "true");
      window.location.reload();
      return;
    }

    // Check if chatId has messages
    const { data } = useApiRequest<ChatWithMessages>("chats/" + chatId);

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

    if (!data.value?.messages || data.value.messages.length === 0) {
      toastMessage.value = "No messages to delete.";
      alertType.value = "error";
      modal.value?.close();
      toastTimeout();
      return;
    }

    useApiRequest("chats/" + chatId, "DELETE");

    localStorage.setItem("toast-message", "Chat deleted successfully!");
    localStorage.setItem("toast-class", "alert-success");
    localStorage.setItem("toast-should-show", "true");

    localStorage.removeItem("chat-id");

    modal.value?.close();

    window.location.reload();
  } catch (e) {
    console.error("Error deleting chat:", e);
    toastMessage.value = "Error deleting chat. Please try again.";
    alertType.value = "error";
    toastTimeout();
  }
};

const openModal = () => {
  modal.value?.showModal();
};

/**
 * Shows the toast message for 4 seconds.
 */
const toastTimeout = () => {
  showToast.value = true;
  setTimeout(() => {
    showToast.value = false;
  }, 4000);
};

const setToastType = (type: string) => {
  switch (type) {
    case "alert-success":
      alertType.value = "success";
      break;
    case "alert-error":
      alertType.value = "error";
      break;
    case "alert-info":
      alertType.value = "info";
      break;
    case "alert-warning":
      alertType.value = "warning";
      break;
  }
};

/**
 * Sets the toast message and class from local storage if it exists.
 * Needed as the window reloads after deleting a chat and for the right order of reload and displaying
 * the toast message, there is a need to set the toast message and class from local storage.
 * - The toast message is shown for 4 seconds.
 * - The toast class is used to set the alert type.
 */
onMounted(() => {
  const shouldShowToast = localStorage.getItem("toast-should-show");

  if (shouldShowToast === "true") {
    toastMessage.value = localStorage.getItem("toast-message") || "";
    toastClass.value = localStorage.getItem("toast-class") || "alert-success";
    toastTimeout();

    setToastType(toastClass.value);

    // cleanup after showing
    localStorage.removeItem("toast-message");
    localStorage.removeItem("toast-class");
    localStorage.removeItem("toast-should-show");
  }
});
</script>
