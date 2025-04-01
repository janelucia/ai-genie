<template>
  <div class="flex flex-col items-center justify-center gap-7">
    <Heading heading="h1" class="">Home Page</Heading>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import {useApiFetch} from "../api/useApiFetch.ts";
import Heading from "../components/Heading.vue";

onMounted(async () => {
  const { fetchData } = useApiFetch('research')
  await fetchData()
})
</script>