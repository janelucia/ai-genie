<template>
  <details class="collapse collapse-plus bg-base-100">
    <summary class="collapse-title font-semibold">{{collapseTitle}}</summary>
    <div class="collapse-content text-sm">
      {{collapseText}}
    </div>
  </details>
</template>
<script setup lang="ts">
defineProps<{
  collapseTitle: string
  collapseText: string
}>()
</script>