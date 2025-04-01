<template>
  <p class="text-base" :class="{'font-bold': button}">
    <slot />
  </p>
</template>
<script setup lang="ts">
defineProps<{
  button?: boolean
}>()
</script>