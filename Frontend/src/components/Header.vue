<template>
  <div
    class="flex w-full justify-between gap-[var(--spacing-in-sections)] items-center fixed bg-base-100 top-0 left-0 z-10 p-4"
  >
    <template v-if="noBack">
      <div class="w-8"></div>
    </template>
    <template v-else>
      <img
        src="../assets/icons/arrow-back.svg"
        alt="Back"
        class="w-8 h-8 cursor-pointer"
        @click="router.go(-1)"
      />
    </template>
    <img
      src="../assets/icons/logo.svg"
      alt="Logo"
      class="cursor-pointer h-10"
    />

    <template v-if="chat">
      <button class="btn btn-primary" @click="openModal">Delete Chat</button>
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

    <div v-if="showToast" class="toast toast-top toast-end">
      <div class="alert" :class="toastClass">
        <span>
          {{ toastMessage }}
        </span>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import router from "../router";
import { ref } from "vue";
import { useApiFetch } from "../api/useApiFetch.ts";
import type { Chat } from "../types/types.ts";

defineProps<{
  chat?: boolean;
  noBack?: boolean;
}>();

const modal = ref<HTMLDialogElement | null>(null);
const toastMessage = ref("");
const toastClass = ref("");
const showToast = ref(false);

const deleteChat = async () => {
  const chatId = localStorage.getItem("chat-id");

  try {
    if (!chatId) {
      toastMessage.value = "No chat ID found.";
      toastClass.value = "alert-error";
      showToast.value = true;
      modal.value?.close();
      return;
    }

    // Check if chatId has messages
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

    if (!data.value?.messages || data.value.messages.length === 0) {
      toastMessage.value = "No messages to delete.";
      toastClass.value = "alert-error";
      showToast.value = true;
      modal.value?.close();
      return;
    }

    await fetch(`http://localhost:8000/api/clear/${chatId}/`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    });
    toastMessage.value = "Chat deleted successfully!";
    toastClass.value = "alert-success";
    localStorage.removeItem("chat-id");

    showToast.value = true;

    modal.value?.close();

    setTimeout(() => {
      showToast.value = false;
      window.location.reload();
    }, 4000);
  } catch (e) {
    console.error("Error deleting chat:", e);
    toastMessage.value = "Error deleting chat. Please try again.";
    toastClass.value = "alert-error";

    showToast.value = true;

    setTimeout(() => {
      showToast.value = false;
    }, 4000);
  }
};

const openModal = () => {
  modal.value?.showModal();
};
</script>
