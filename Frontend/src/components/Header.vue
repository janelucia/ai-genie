<template>
  <div
    class="flex w-full justify-between gap-[var(--spacing-in-sections)] items-center fixed bg-base-100 top-0 left-0 z-10 p-4"
  >
    <button class="btn btn-secondary" @click="router.go(-1)">
      <Text>Back</Text>
    </button>
    <Text class="flex-grow text-center font-bold"> Oslo Met AI Lab </Text>
    <FloatChatButton />
  </div>
</template>
<script setup lang="ts">
import router from "../router";
import Text from "./Text.vue";
import FloatChatButton from "./FloatChatButton.vue";

defineProps<{
  headerTitle: string;
}>();
</script>
