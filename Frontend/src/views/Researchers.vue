<template>
  <Header headerTitle="Researchers" />
  <div class="pt-24 flex flex-col items-center justify-center gap-7">
    <Card
      v-for="researcher in result"
      :key="researcher.id"
      card-image="https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp"
      card-image-alt="Some Profile Picture"
      :card-title="`${researcher.firstname} ${researcher.surname}`"
      button-title="Learn more"
      :link="'/researchers/' + researcher.id.toString()"
      card-text="This is a placeholder text for the researcher description. It should be replaced with the actual researcher description."
      vertical
    />
  </div>
</template>
<script setup lang="ts">
import Card from "../components/Card.vue";
import { ref, watch } from "vue";
import { useApiFetch } from "../api/useApiFetch.ts";
import type { Researchers } from "../types/types.ts";
import Header from "../components/Header.vue";

const result = ref<Researchers[]>([]);

const { data } = useApiFetch<Researchers[]>("researchers");

watch(data, () => {
  if (data.value) {
    result.value = data.value;
  }
});
</script>
