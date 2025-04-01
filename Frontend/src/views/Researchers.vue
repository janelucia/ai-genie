<template>
  <div class="flex flex-col items-center justify-center gap-7">
    <Heading heading="h1" class="">Researchers</Heading>
    <Card v-for="researcher in result" :key="researcher.id"
        card-image="https://http.cat/status/200.jpg"
        card-image-alt="Cats"
        :card-title="`${researcher.firstname} ${researcher.surname}`"
        button-title="Learn more"
        vertical
    />
  </div>
</template>
<script setup lang="ts">
import Card from "../components/Card.vue";
import Heading from "../components/Heading.vue";
import {ref, watch} from "vue";
import {useApiFetch} from "../api/useApiFetch.ts";

type Researchers = {
  id: number;
  firstname: string;
  surname: string;
  "related_research": number;
}

const result = ref<Researchers[]>([]);

const { data } = useApiFetch<Researchers[]>('researchers')

watch(data, () => {
  if (data.value) {
    result.value = data.value
  }
})
</script>