<template>
  <div class="flex flex-col items-center justify-center gap-7">
    <Heading heading="h1" class="">Events</Heading>
    <Card
        card-image="https://http.cat/status/200.jpg"
        card-image-alt="Cats"
        card-title="Event A!"
        card-text="This is a very nice event! It is very nice! Just like the other events! It is very nice! Just like the other events! It is very nice! Just like the other events! It is very nice! Just like the other events!"
        button-title="Sign up"
        vertical
    />
  </div>
</template>
<script setup lang="ts">
import Card from "../components/Card.vue";
import Heading from "../components/Heading.vue";
</script>