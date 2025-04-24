<template>
  <div class="fixed bottom-0 z-10 pt-2 w-full bg-base-100">
    <nav
      class="bg-primary w-full flex justify-center rounded-tl-lg rounded-tr-lg"
    >
      <ul class="menu menu-horizontal flex-nowrap">
        <li class="w-12 h-12">
          <router-link class="w-full h-full" to="/">
            <img
              src="../assets/icons/home.svg"
              alt="Home"
              class="w-full h-full"
            />
          </router-link>
        </li>
        <li class="w-12 h-12">
          <router-link class="w-full h-full" to="/events">
            <img
              src="../assets/icons/events.svg"
              alt="Events"
              class="w-full h-full"
            />
          </router-link>
        </li>
        <li class="w-12 h-12">
          <router-link class="w-full h-full" to="/chat">
            <img
              src="../assets/icons/chat.svg"
              alt="Chat"
              class="w-full h-full"
            />
          </router-link>
        </li>
        <li class="w-12 h-12">
          <router-link class="w-full h-full block" to="/research">
            <img
              src="../assets/icons/research.svg"
              alt="Research"
              class="w-full h-full block"
            />
          </router-link>
        </li>
        <li class="w-12 h-12">
          <router-link class="w-full h-full block" to="/researchers">
            <img
              src="../assets/icons/researcher.svg"
              alt="Researchers"
              class="w-full h-full block"
            />
          </router-link>
        </li>
      </ul>
    </nav>
  </div>
</template>
