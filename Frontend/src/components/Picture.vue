<template>
  <figure>
    <div class="relative w-full h-full rounded-lg">
      <img
        :src="image"
        :alt="imageAlt"
        class="w-full h-full object-cover"
        :class="pictureClass"
      />
    </div>
  </figure>
</template>
<script setup lang="ts">
defineProps<{
  image: string;
  imageAlt: string;
  tooltipText?: string;
  pictureClass?: string;
}>();
</script>
