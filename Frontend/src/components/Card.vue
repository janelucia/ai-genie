<template>
  <div class="card bg-base-100 w-full gap-[var(--spacing-in-sections)]" :class="{'card-side': vertical}">
    <figure :class="{'h-28': !vertical}">
      <img
          :src="cardImage"
          :alt="cardImageAlt" />
    </figure>
    <div class="card-body p-0 gap-[var(--spacing-in-sections)]" :class="{'pr-[var(--spacing-in-sections)]': vertical}">
      <Heading heading="h2" class="card-title" :class="{'pl-4': !vertical}">{{cardTitle}}</Heading>
      <Text v-if="cardText" class=" line-clamp-3" :class="{'pl-4': !vertical}">{{cardText}}</Text>
      <Text v-if="cardDate" class=" line-clamp-3" :class="{'pl-4': !vertical}">{{formattedDate}}</Text>
      <Text v-if="cardDate" class=" line-clamp-3" :class="{'pl-4': !vertical}">{{formattedTime}}</Text>
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
import {computed} from "vue";

const props = defineProps<{
  cardImage: string
  cardImageAlt: string
  cardTitle: string
  cardText?: string
  cardDate?: string
  buttonTitle: string
  vertical?: boolean
}>()

const formattedDate = computed(() => {
  if (props.cardDate) {
    return new Intl.DateTimeFormat('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    }).format(new Date(props.cardDate));
  }
  return '';
});

const formattedTime = computed(() => {
  if (props.cardDate) {
    return new Intl.DateTimeFormat('en-US', {
      hour: 'numeric',
      minute: 'numeric',
    }).format(new Date(props.cardDate));
  }
  return '';
});
</script>