<template>
  <div class="flex flex-wrap gap-[var(--spacing-in-sections)] self-start">
    <div
      v-for="keyword in keywords"
      :key="keyword"
      class="badge badge-outline text-base-content badge-secondary"
    >
      {{ keyword }}
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  keywords: string[];
}>();
</script>
