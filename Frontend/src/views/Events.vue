<template>
  <Header headerTitle="Research" />
  <div class="pt-20 flex flex-col items-center justify-center gap-7">
    <Card v-for="event in result" :key="event.id"
        card-image="https://http.cat/status/200.jpg"
        card-image-alt="Cats"
        :card-title="event.name"
        :card-date="event.date"
        button-title="Sign up"
        :link="`/events/${event.id}`"
        vertical
    />
  </div>
</template>
<script setup lang="ts">
import Card from "../components/Card.vue";
import {ref, watch} from "vue";
import {useApiFetch} from "../api/useApiFetch.ts";
import type {Events} from "../types/types.ts";
import Header from "../components/Header.vue";

const result = ref<Events[]>([]);

const { data } = useApiFetch<Events[]>('events')

watch(data, () => {
  if (data.value) {
    result.value = data.value
  }
})
</script>