<template>
  <div>
    <NavBar/>
    <main class="m-4">
      <router-view />
    </main>
  </div>
</template>
<script setup lang="ts">
import NavBar from "./components/NavBar.vue";
</script>