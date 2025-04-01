<template>
  <div class="card bg-base-100 w-full shadow-sm gap-4" :class="{'card-side': vertical}">
    <figure :class="{'w-1/3': vertical, 'h-28': !vertical}">
      <img
          :src="cardImage"
          :alt="cardImageAlt" />
    </figure>
    <div class="card-body p-0">
      <Heading heading="h2" class="card-title pl-4">{{cardTitle}}</Heading>
      <Text class="pl-4">{{cardText}}</Text>
      <div class="card-actions pt-4" :class="{'pl-4': vertical}">
        <button class="btn btn-primary w-full">{{buttonTitle}}</button>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import Text from "./Text.vue";
import Heading from "./Heading.vue";

defineProps<{
  cardImage: string
  cardImageAlt: string
  cardTitle: string
  cardText: string
  buttonTitle: string,
  vertical?: boolean
}>()
</script>