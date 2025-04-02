<template>
  <div class="flex w-full justify-between">
    <button class="btn btn-secondary" @click="router.go(-1)">
      <Text>Back</Text>
    </button>
    <Heading heading="h1" class="flex-grow text-center">
      {{headerTitle}}
    </Heading>
    <div class="w-16"></div>
  </div>
</template>
<script setup lang="ts">
import router from "../router";
import Text from "./Text.vue";
import Heading from "./Heading.vue";

defineProps<{
  headerTitle: string
}>();
</script>