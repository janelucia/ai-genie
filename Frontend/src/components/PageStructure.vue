<template>
  <Header :no-back="noBack" />
  <div class="py-14 flex flex-col gap-[var(--spacing-between-sections)] w-full">
    <Heading v-if="title" heading="h1" class="text-center">
      {{ title }}
    </Heading>
    <slot />
  </div>
</template>
<script setup lang="ts">
import Header from "./Header.vue";
import Heading from "./Heading.vue";
defineProps<{
  title?: string;
  noBack?: boolean;
}>();
</script>
