<template>
  <div class="card bg-base-100 w-full gap-[var(--spacing-in-sections)]" :class="{'card-side': vertical}">
    <figure :class="vertical ? 'w-28 overflow-hidden flex-shrink-0' : 'h-40 w-full overflow-hidden'">
      <img
          :src="cardImage"
          :alt="cardImageAlt"
          class="w-full h-full object-cover"
      />
    </figure>


    <div class="card-body p-0 gap-[var(--spacing-in-sections)]" :class="{'pr-[var(--spacing-in-sections)]': vertical}">
      <Heading heading="h2" class="card-title" :class="{'pl-4': !vertical}">{{cardTitle}}</Heading>
      <Text v-if="cardText" class=" line-clamp-3" :class="{'pl-4': !vertical}">{{cardText}}</Text>
      <div v-if="cardDate" class="flex gap-[var(--spacing-in-sections)] items-center justify-center whitespace-nowrap">
        <Text :class="{'pl-4': !vertical}">{{formattedDate}}</Text>
        <Text :class="{'pl-4': !vertical}">{{formattedTime}}</Text>
      </div>
      <div class="card-actions">
        <button class="btn btn-primary w-full whitespace-nowrap" @click="router.push(link)">
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
import router from "../router";
import {formatDate, formatTime} from "../utils/dateUtils.ts";

const props = defineProps<{
  cardImage: string
  cardImageAlt: string
  cardTitle: string
  cardText?: string
  cardDate?: string
  buttonTitle: string
  link?: string
  vertical?: boolean
}>()

const formattedDate = computed(() => {
  if (props.cardDate) {
    return formatDate(props.cardDate);
  }
  return '';
});

const formattedTime = computed(() => {
  if (props.cardDate) {
    return formatTime(props.cardDate);
  }
  return '';
});
</script>