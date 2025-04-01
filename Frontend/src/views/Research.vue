<template>
  <div class="flex flex-col items-center justify-center gap-7">
    <Heading heading="h1" class="">Research</Heading>
    <Card v-for="research in result" :key="research.id"
        card-image="https://http.cat/status/200.jpg"
        card-image-alt="Cats"
        :card-title="research.name"
        :card-text="research.summary"
        button-title="Learn more"
    />
  </div>
</template>
<script setup lang="ts">
import Card from "../components/Card.vue";
import Heading from "../components/Heading.vue";
import {ref, watch} from "vue";
import {useApiFetch} from "../api/useApiFetch.ts";

type Research = {
  id: number;
  name: string;
  summary: string;
  "source_file": string;
}

const result = ref<Research[]>([]);

const { data } = useApiFetch<Research[]>('research')

watch(data, () => {
  if (data.value) {
    result.value = data.value
  }
})
</script>