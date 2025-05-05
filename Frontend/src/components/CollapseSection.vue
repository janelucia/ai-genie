<template>
  <details class="collapse collapse-plus" :open="open">
    <summary class="collapse-title pl-0">
      <Heading heading="h3">{{ collapseTitle }}</Heading>
    </summary>
    <div class="collapse-content w-full p-0">
      <slot />
    </div>
  </details>
</template>
<script setup lang="ts">
import Heading from "./Heading.vue";

defineProps<{
  collapseTitle: string;
  open?: boolean;
}>();
</script>
