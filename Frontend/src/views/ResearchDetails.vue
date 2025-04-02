<template>
  <div class="flex flex-col items-center justify-center gap-7">
  <Header :header-title="'Research ' + id"/>
  </div>
</template>
<script setup lang="ts">
import { useRoute } from 'vue-router'
import {ref, watch} from "vue";
import {useApiFetch} from "../api/useApiFetch.ts";
import Header from "../components/Header.vue";

type ResearchIndividual = {
  id: number;
  name: string;
  summary: string;
  "source_file": string;
}

const route = useRoute()
const id = route.params.id

const result = ref<ResearchIndividual[]>([]);

const { data } = useApiFetch<ResearchIndividual[]>('research/' +  id)

watch(data, () => {
  if (data.value) {
    result.value = data.value
  }
})
</script>