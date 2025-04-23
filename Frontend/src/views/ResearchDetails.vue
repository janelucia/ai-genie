<template>
  <Header :header-title="'Research ' + id" />
  <div class="pt-24 flex flex-col items-center justify-center gap-7 w-full">
    <Heading heading="h1" class="text-center">
      {{ result.name }}
    </Heading>
    <PictureWithToolTip
      :image="ResearchBanner"
      image-alt="ResearchBanner"
      tooltip-text="This image was created using AI and has no relation to the research."
      picture-class="rounded"
    />
    <div
      v-if="relatedResearchers.length"
      class="carousel overflow-x-auto max-w-full px-4 space-x-4"
    >
      <div
        v-for="researcher in relatedResearchers"
        :key="researcher.id"
        class="carousel-item w-24 shrink-0 flex flex-col items-center"
      >
        <button @click="router.push(`/researchers/${researcher.id}`)">
          <Avatar class="w-24" />
        </button>
        <Text small class="text-center">
          {{ researcher.firstname }} {{ researcher.surname }}
        </Text>
      </div>
    </div>
    <Text class="w-full">{{ result.summary }}</Text>
    <Keywords :keywords="keywordsStringToArray(result.keywords)" />
    <CollapseSection collapse-title="Abstract">
      <Text class="break-words break-all whitespace-pre-wrap">
        This section is currently under construction!
      </Text>
    </CollapseSection>
    <a
      :href="'http://localhost:8000' + result.source_file"
      download
      target="_blank"
      class="btn btn-accent text-base-100 w-full"
    >
      Download Paper
    </a>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from "vue-router";
import { ref, watch } from "vue";
import { useApiFetch } from "../api/useApiFetch.ts";
import Header from "../components/Header.vue";
import Text from "../components/Text.vue";
import type { Research, Researchers } from "../types/types.ts";
import CollapseSection from "../components/CollapseSection.vue";
import router from "../router";
import Avatar from "../components/Avatar.vue";
import Keywords from "../components/Keywords.vue";
import Heading from "../components/Heading.vue";
import PictureWithToolTip from "../components/PictureWithToolTip.vue";
import ResearchBanner from "../assets/img/research-paper-banner-ai.png";

const route = useRoute();
const id = route.params.id;

const result = ref<Research>({
  id: 0,
  name: "",
  summary: "",
  keywords: "",
  source_file: "",
});

const relatedResearchers = ref<Researchers[]>([]);

const { data: researchData } = useApiFetch<Research>("research/" + id);
const { data: researchersData } = useApiFetch<Researchers[]>("researchers");

watch(researchData, () => {
  if (researchData.value) {
    result.value = researchData.value;
  }
});

watch(researchersData, () => {
  if (researchersData.value) {
    relatedResearchers.value = researchersData.value.filter(
      (researcher) =>
        Array.isArray(researcher.related_research) &&
        researcher.related_research.includes(Number(id)),
    );
  }
});

const keywordsStringToArray = (keywords: string | undefined): string[] =>
  keywords ? keywords.split(",").map((keyword) => keyword.trim()) : [];
</script>
