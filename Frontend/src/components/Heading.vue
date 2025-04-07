<template>
  <component :is="headingTag" :class="headingClass">
    <slot />
  </component>
</template>

<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{
  heading: "h1" | "h2" | "h3";
}>();

const headingTag = computed(() => props.heading);

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
