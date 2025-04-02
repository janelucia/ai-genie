<template>
  <div class="flex flex-col items-center justify-center gap-7">
    <Heading heading="h1" class="">Events</Heading>
    <Card v-for="event in result" :key="event.id"
        card-image="https://http.cat/status/200.jpg"
        card-image-alt="Cats"
        :card-title="event.name"
        :card-date="event.date"
        button-title="Sign up"
        vertical
    />
  </div>
</template>
<script setup lang="ts">
import Card from "../components/Card.vue";
import Heading from "../components/Heading.vue";
import {ref, watch} from "vue";
import {useApiFetch} from "../api/useApiFetch.ts";
import type {Events} from "../types/types.ts";

const result = ref<Events[]>([]);

const { data } = useApiFetch<Events[]>('events')

watch(data, () => {
  if (data.value) {
    result.value = data.value
  }
})
</script>