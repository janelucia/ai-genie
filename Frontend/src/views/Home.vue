<template>
  <div class="flex flex-col items-center justify-center gap-7">
    <h1 class="">Home Page</h1>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import {useApiFetch} from "../api/useApiFetch.ts";

onMounted(async () => {
  const { fetchData } = useApiFetch('research')
  await fetchData()
})
</script>