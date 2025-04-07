<template>
  <div>
    <NavBar />
    <main class="p-4 mb-14">
      <router-view />
    </main>
  </div>
</template>
<script setup lang="ts">
import NavBar from "./components/NavBar.vue";
</script>
