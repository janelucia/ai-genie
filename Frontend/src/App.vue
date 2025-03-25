<template>
  <div>
    <nav>
      <router-link to="/">Home</router-link> |
      <router-link to="/search">Search</router-link> |
      <router-link to="/chat">Chat</router-link> |
      <router-link to="/events">Events</router-link> |
      <router-link to="/bookmarks">Bookmarks</router-link>
    </nav>

    <router-view />
  </div>
</template>
