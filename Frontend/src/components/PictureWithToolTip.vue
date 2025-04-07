<template>
  <figure>
    <div class="relative w-full h-full rounded-lg">
      <img
        :src="image"
        :alt="imageAlt"
        class="w-full h-full object-cover"
        :class="pictureClass"
      />

      <div
        v-if="tooltipText"
        class="absolute bottom-2 right-2 tooltip tooltip-info tooltip-left"
        :data-tip="tooltipText"
      >
        <button class="btn btn-xs btn-circle btn-info">
          <Text> i </Text>
        </button>
      </div>
    </div>
  </figure>
</template>
<script setup lang="ts">
import Text from "./Text.vue";

defineProps<{
  image: string;
  imageAlt: string;
  tooltipText?: string;
  pictureClass?: string;
}>();
</script>
