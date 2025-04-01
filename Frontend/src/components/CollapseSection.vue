<template>
  <details class="collapse collapse-plus bg-base-100">
    <summary class="collapse-title font-semibold">
      <Heading heading="h3">{{collapseTitle}}</Heading>
    </summary>
    <div class="collapse-content text-sm">
      <Text>
        {{collapseText}}
      </Text>
    </div>
  </details>
</template>
<script setup lang="ts">
import Heading from "./Heading.vue";
import Text from "./Text.vue";

defineProps<{
  collapseTitle: string
  collapseText: string
}>()
</script>