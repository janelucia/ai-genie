<template>
  <div class="avatar">
    <img
      :src="img"
      class="w-full object-cover rounded-full"
      alt="Some avatar"
    />
  </div>
</template>

<script setup lang="ts">
import { defineProps } from "vue";
defineProps<{
  img?: string;
}>();
</script>
