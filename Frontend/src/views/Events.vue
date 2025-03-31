<template>
  <div class="flex flex-col items-center justify-center gap-7">
    <h1 class="">Events</h1>
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
import Card from "../components/Card.vue";
</script>