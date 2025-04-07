<template>
  <p class="text-base" :class="{ 'font-bold': button, 'text-sm': small }">
    <slot />
  </p>
</template>
<script setup lang="ts">
defineProps<{
  button?: boolean;
  small?: boolean;
}>();
</script>
