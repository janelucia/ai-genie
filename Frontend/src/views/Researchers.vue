<template>
  <PageStructure title="Researchers">
    <div
      class="w-full flex justify-between items-center gap-[var(--spacing-in-sections)]"
    >
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
      <FilterModal
        v-if="data?.find((d) => d.keywords)"
        ref="keywordModal"
        :keywords="data?.map((d) => d.keywords ?? '') ?? []"
        @filter="applyKeywordFilter"
      />
    </div>
    <Card
      v-for="researcher in filteredResults"
      :key="researcher.id"
      card-image="https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp"
      card-image-alt="Some Profile Picture"
      :card-title="`${researcher.firstname} ${researcher.surname}`"
      button-title="Learn more"
      :link="'/researchers/' + researcher.id.toString()"
      :card-text="researcher.about"
      vertical
    />
  </PageStructure>
</template>
<script setup lang="ts">
import Card from "../components/Card.vue";
import { computed, ref, watch } from "vue";
import { useApiFetch } from "../api/useApiFetch.ts";
import type { Researchers } from "../types/types.ts";
import PageStructure from "../components/PageStructure.vue";
import FilterModal from "../components/FilterModal.vue";
import useSearchAndFilter from "../../composables/useSearchAndFilter.ts";

const keywordModal = ref();

const { data } = useApiFetch<Researchers[]>("researchers");

const { searchQuery, filteredResults, applyKeywordFilter } = useSearchAndFilter(
  computed(() => data.value ?? []),
  (researcher: Researchers) => [researcher.firstname, researcher.surname],
);
</script>
