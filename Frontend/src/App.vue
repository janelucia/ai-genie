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

<script setup lang="ts"> 
  import { ref, onMounted } from 'vue'
  
  const data = ref(null);
  const error = ref(null);
  
  onMounted(async() => {
    try {
      const response = await fetch('http://localhost:8000/research/')
      
      if (!response.ok) throw new Error('Network response was not ok')
        const result = await response.json()
        data.value = result
    } catch (err) {
      error.value = err.message
    } finally{
      console.log(data)
    }
  
  })
</script>