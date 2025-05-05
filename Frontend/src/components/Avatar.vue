<template>
  <div class="avatar">
    <img
      :src="
        img
          ? img
          : 'https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp'
      "
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
