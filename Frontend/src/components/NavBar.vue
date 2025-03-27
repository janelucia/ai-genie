<template>
  <nav class="bg-primary w-full flex justify-center rounded-tl-lg rounded-tr-lg fixed bottom-0 h-12">
    <ul class="menu menu-horizontal">
      <li>
        <router-link to="/">Home</router-link>
      </li>
      <li>
        <router-link to="/search">Search</router-link>
      </li>
      <li>
        <router-link to="/chat">Chat</router-link>
      </li>
      <li>
        <router-link to="/events">Events</router-link>
      </li>
      <li>
        <router-link to="/bookmarks">Bookmarks</router-link>
      </li>
    </ul>
  </nav>
</template>
