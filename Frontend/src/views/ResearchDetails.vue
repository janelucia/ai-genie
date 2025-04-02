<template>
  <Heading heading="h3">Research {{id}}</Heading>
</template>
<script setup lang="ts">
import Heading from "../components/Heading.vue";
import { useRoute } from 'vue-router'

const route = useRoute()
const id = route.params.id
</script>