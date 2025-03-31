<template>
  <nav class="bg-primary w-full flex justify-center rounded-tl-lg rounded-tr-lg fixed bottom-0 h-12 z-10">
    <ul class="menu menu-horizontal">
      <li>
        <router-link to="/">Home</router-link>
      </li>
      <li>
        <router-link to="/events">Events</router-link>
      </li>
      <li>
        <router-link to="/research">Research</router-link>
      </li>
      <li>
        <router-link to="/researchers">Researchers</router-link>
      </li>
    </ul>
  </nav>
</template>
<script setup lang="ts">
</script>