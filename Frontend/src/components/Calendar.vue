<template>
  <calendar-date
    class="cally bg-base-100 border border-base-300 shadow-lg rounded-box w-full text-lg"
  >
    <template v-slot:previous>
      <svg
        aria-label="Previous"
        class="fill-current size-4"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
      >
        <path fill="currentColor" d="M15.75 19.5 8.25 12l7.5-7.5" />
      </svg>
    </template>

    <template v-slot:next>
      <svg
        aria-label="Next"
        class="fill-current size-4"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
      >
        <path fill="currentColor" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
      </svg>
    </template>

    <calendar-month></calendar-month>
  </calendar-date>
</template>
<script setup lang="ts">
import "cally";
</script>
