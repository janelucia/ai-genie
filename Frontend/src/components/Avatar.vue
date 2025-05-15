<template>
  <div class="avatar">
    <img
      :src="img"
      class="w-full object-cover rounded-full"
      :alt="'Picture of ' + name"
    />
  </div>
</template>

<script setup lang="ts">
defineProps<{
  img?: string;
  name?: string;
}>();
</script>
