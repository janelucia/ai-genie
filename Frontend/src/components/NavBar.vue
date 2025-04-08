<template>
  <div class="fixed bottom-0 z-10 pt-2 w-full bg-base-100">
    <nav
      class="bg-primary w-full flex justify-center rounded-tl-lg rounded-tr-lg"
    >
      <ul class="menu menu-horizontal flex-nowrap">
        <li>
          <router-link to="/">
            <Text>Home</Text>
          </router-link>
        </li>
        <li>
          <router-link to="/events">
            <Text>Events</Text>
          </router-link>
        </li>
        <li>
          <router-link to="/research">
            <Text>Research</Text>
          </router-link>
        </li>
        <li>
          <router-link to="/researchers">
            <Text>Researchers</Text>
          </router-link>
        </li>
      </ul>
    </nav>
  </div>
</template>
<script setup lang="ts">
import Text from "./Text.vue";
</script>
