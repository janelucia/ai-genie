<template>
  <div
    class="card bg-base-100 w-full gap-[var(--spacing-in-sections)]"
    :class="{ 'card-side': vertical }"
  >
    <Picture
      :image="cardImage"
      :image-alt="cardImageAlt"
      :tooltip-text="tooltipText"
      :class="vertical ? 'w-28 flex-shrink-0' : 'h-40 w-full'"
    />

    <div
      class="card-body p-0 gap-[var(--spacing-in-sections)]"
      :class="{ 'pr-[var(--spacing-in-sections)]': vertical }"
    >
      <Heading heading="h3" class="card-title" :class="{ 'pl-4': !vertical }">{{
        cardTitle
      }}</Heading>
      <div
        v-if="cardDate"
        class="flex gap-[var(--spacing-in-sections)] justify-center"
      >
        <Text>🗓️</Text>
        <Text :class="{ 'pl-4 whitespace-nowrap': !vertical }">
          {{ formattedDate }}, {{ formattedTime }}</Text
        >
      </div>
      <Text
        v-if="cardText"
        class="line-clamp-3"
        :class="{ 'pl-4': !vertical }"
        >{{ cardText }}</Text
      >
      <div class="card-actions">
        <button
          v-if="link"
          class="btn btn-secondary w-full whitespace-nowrap"
          :class="buttonClass"
          @click="router.push(link)"
        >
          <Text button>{{ buttonTitle }}</Text>
        </button>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import Text from "./Text.vue";
import Heading from "./Heading.vue";
import { computed } from "vue";
import router from "../router";
import { formatDate, formatTime } from "../utils/dateUtils.ts";
import Picture from "./Picture.vue";

const props = defineProps<{
  cardImage: string;
  cardImageAlt: string;
  cardTitle: string;
  cardText?: string;
  cardDate?: Date | string;
  buttonTitle?: string;
  buttonClass?: string;
  link?: string;
  tooltipText?: string;
  vertical?: boolean;
}>();

const formattedDate = computed(() => {
  if (props.cardDate) {
    return formatDate(props.cardDate);
  }
  return "";
});

const formattedTime = computed(() => {
  if (props.cardDate) {
    return formatTime(props.cardDate);
  }
  return "";
});
</script>
