<template>
  <details class="collapse collapse-plus">
    <summary class="collapse-title font-semibold">
      <Heading heading="h3">{{collapseTitle}}</Heading>
    </summary>
    <div class="collapse-content w-full">
      <Text class="break-words break-all whitespace-pre-wrap">
        <slot />
      </Text>
    </div>
  </details>
</template>
<script setup lang="ts">
import Heading from "./Heading.vue";
import Text from "./Text.vue";

defineProps<{
  collapseTitle: string
}>()
</script>