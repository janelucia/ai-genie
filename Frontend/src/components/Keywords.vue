<template>
  <div class="flex gap-[var(--spacing-in-sections)]">
    <div v-for="keyword in keywords" :key="keyword" class="badge badge-outline text-base-content badge-primary">{{keyword}}</div>
  </div>
</template>

<script setup lang="ts">
  defineProps<{
    keywords: string[]
  }>()
</script>