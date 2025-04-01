<template>
  <div class="flex flex-col items-center justify-center gap-7">
    <Heading heading="h1" class="">Research</Heading>
    <Card
        card-image="https://http.cat/status/200.jpg"
        card-image-alt="Cats"
        card-title="Cats!"
        card-text="Cats are great!"
        button-title="Cuddle now"
    />
  </div>
</template>
<script setup lang="ts">
import Card from "../components/Card.vue";
import Heading from "../components/Heading.vue";
</script>