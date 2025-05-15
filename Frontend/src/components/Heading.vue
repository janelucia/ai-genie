<template>
  <component :is="headingTag" class="text-secondary" :class="headingClass">
    <slot />
  </component>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { HeadingType } from "../types/types";

const props = defineProps<{
  heading: HeadingType;
}>();

const headingTag = computed(() => props.heading);

/**
 * Returns the class for the heading based on the heading type. Enables a standardised design across the entire application.
 */
const headingClass = computed(() => {
  switch (props.heading) {
    case "h1":
      return "text-3xl font-bold";
    case "h2":
      return "text-2xl font-semibold";
    case "h3":
      return "text-xl font-semibold";
    default:
      return "";
  }
});
</script>
