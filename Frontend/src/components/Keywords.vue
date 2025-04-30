<template>
  <div class="flex flex-wrap gap-[var(--spacing-in-sections)] self-start">
    <div
      v-for="keyword in keywords"
      :key="keyword"
      class="badge badge-outline badge-secondary"
      @click="router.push('/research?keywords=' + keyword)"
    >
      {{ keyword }}
    </div>
  </div>
</template>

<script setup lang="ts">
import router from "../router";

defineProps<{
  keywords: string[];
}>();
</script>
