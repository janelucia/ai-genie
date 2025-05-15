<template>
  <div class="fixed bottom-0 z-10 pt-2 w-full bg-base-100">
    <nav
      class="bg-primary w-full flex justify-center rounded-tl-lg rounded-tr-lg"
    >
      <ul class="menu menu-horizontal flex-nowrap justify-evenly w-full">
        <li v-for="(link, index) in links" :key="index">
          <router-link
            :to="link.to"
            class="w-full h-full flex items-center justify-center"
          >
            <img
              :src="link.icon"
              :alt="link.alt"
              class="w-8 h-8 object-contain aspect-square"
            />
          </router-link>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script setup lang="ts">
const links = [
  { to: "/", icon: "/icons/home.svg", alt: "Home Icon" },
  { to: "/events", icon: "/icons/events.svg", alt: "Events Icon" },
  { to: "/chat", icon: "/icons/chat.svg", alt: "Chat Icon" },
  { to: "/research", icon: "/icons/research.svg", alt: "Research Icon" },
  {
    to: "/researchers",
    icon: "/icons/researcher.svg",
    alt: "Researchers Icon",
  },
];
</script>
