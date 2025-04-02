<template>
  <div class="flex flex-col items-center justify-center gap-7">
    <Header :header-title="'Researcher ' + id"/>
  </div>
</template>
<script setup lang="ts">
import { useRoute } from 'vue-router'
import Header from "../components/Header.vue";

const route = useRoute()
const id = route.params.id
</script>