<template>
  <div>
    Hello
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