<template>
  <Header headerTitle="Researchers" />
  <div class="pt-14 flex flex-col items-center justify-center gap-7">
    <Heading heading="h1" class="text-center">Researchers</Heading>
    <label class="input w-full">
      <svg
        class="h-[1em] opacity-50"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
      >
        <g
          stroke-linejoin="round"
          stroke-linecap="round"
          stroke-width="2.5"
          fill="none"
          stroke="currentColor"
        >
          <circle cx="11" cy="11" r="8"></circle>
          <path d="m21 21-4.3-4.3"></path>
        </g>
      </svg>
      <input
        v-model="searchQuery"
        type="search"
        class="grow"
        placeholder="Search"
      />
    </label>
    <Card
      v-for="researcher in filteredResults"
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
import { computed, ref, watch } from "vue";
import { useApiFetch } from "../api/useApiFetch.ts";
import type { Researchers } from "../types/types.ts";
import Header from "../components/Header.vue";
import Heading from "../components/Heading.vue";

const searchQuery = ref("");
const result = ref<Researchers[]>([]);

const { data } = useApiFetch<Researchers[]>("researchers");

watch(data, () => {
  if (data.value) {
    result.value = data.value;
  }
});

const filteredResults = computed(() => {
  return result.value.filter(
    (research) =>
      research.firstname
        .toLowerCase()
        .includes(searchQuery.value.toLowerCase()) ||
      research.surname.toLowerCase().includes(searchQuery.value.toLowerCase()),
  );
});
</script>
