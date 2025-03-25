<template><h1>Home Page</h1></template>

<script setup lang="ts">
import { onMounted } from 'vue'
import {useApiFetch} from "../api/useApiFetch.ts";

onMounted(async () => {
  const { fetchData } = useApiFetch('research')
  await fetchData()
})
</script>