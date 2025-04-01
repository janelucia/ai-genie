<template>
  <div class="card bg-base-100 w-full gap-[var(--spacing-in-sections)]" :class="{'card-side': vertical}">
    <figure :class="{'h-28': !vertical}">
      <img
          :src="cardImage"
          :alt="cardImageAlt" />
    </figure>
    <div class="card-body p-0 gap-[var(--spacing-in-sections)]" :class="{'pr-[var(--spacing-in-sections)]': vertical}">
      <Heading heading="h2" class="card-title" :class="{'pl-4': !vertical}">{{cardTitle}}</Heading>
      <Text class=" line-clamp-3" :class="{'pl-4': !vertical}">{{cardText}}</Text>
      <div class="card-actions">
        <button class="btn btn-primary w-full">
          <Text button>{{buttonTitle}}</Text>
        </button>
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