<template>
  <div class="flex flex-col items-center justify-center gap-7 w-full overflow-hidden">
    <Header :header-title="'Research ' + id" />

    <div
        v-if="relatedResearchers.length"
        class="carousel overflow-x-auto space-x-4 max-w-screen-sm gap-[var(--spacing-in-sections)]"
    >
      <div
          v-for="researcher in relatedResearchers"
          :key="researcher.id"
          class="carousel-item m-0 shrink-0 flex flex-col items-center justify-center"
      >
          <div class="avatar">
            <div class="w-24 rounded-full">
              <img
                  src="https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp"
                  class="w-full object-cover"
                  alt="Some avatar"
              />
            </div>
          </div>
          <Text small class="text-center">
            {{ researcher.firstname }} {{ researcher.surname }}
          </Text>
      </div>
    </div>
    <div class="flex gap-[var(--spacing-in-sections)]">
      <div class="badge badge-outline text-base-content badge-primary">Keyword 1</div>
      <div class="badge badge-outline text-base-content badge-primary">Keyword 2</div>
      <div class="badge badge-outline text-base-content badge-primary">Keyword 3</div>
    </div>
  </div>
</template>


<script setup lang="ts">
import { useRoute } from 'vue-router'
import { ref, watch } from 'vue';
import { useApiFetch } from '../api/useApiFetch.ts';
import Header from '../components/Header.vue';
import Text from '../components/Text.vue';
import type { Research, Researchers } from '../types/types.ts';

const route = useRoute();
const id = route.params.id;

const result = ref<Research[]>([]);
const relatedResearchers = ref<Researchers[]>([]);

const { data: researchData } = useApiFetch<Research[]>('research/' + id);
const { data: researchersData } = useApiFetch<Researchers[]>('researchers');

watch(researchData, () => {
  if (researchData.value) {
    result.value = researchData.value;
  }
});

watch(researchersData, () => {
  if (researchersData.value) {
    relatedResearchers.value = researchersData.value.filter(
        researcher =>
            Array.isArray(researcher.related_research) &&
            researcher.related_research.includes(Number(id))
    );
  }
});
</script>