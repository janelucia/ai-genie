<template>
  <div class="flex flex-col items-center justify-center gap-7">
    <h1 class="">Home Page</h1>
    <Card
        card-image="https://http.cat/status/200.jpg"
        card-image-alt="Cats"
        card-title="Cats!"
        card-text="Cats are great!"
        button-title="Cuddle now"
    />
    <Card
        card-image="https://http.cat/status/200.jpg"
        card-image-alt="Cats"
        card-title="Cats!"
        card-text="Cats are great!"
        button-title="Cuddle now"
        vertical
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import {useApiFetch} from "../api/useApiFetch.ts";
import Card from "../components/Card.vue";

onMounted(async () => {
  const { fetchData } = useApiFetch('research')
  await fetchData()
})
</script>