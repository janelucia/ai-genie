<template>
  <Header :header-title="'Researcher ' + id" />
  <div class="pt-24 flex flex-col gap-7">
    <div
      class="flex items-center justify-evenly w-full gap-[var(--spacing-in-sections)]"
    >
      <Avatar class="w-32" />
      <div>
        <Heading heading="h1">
          {{ result.firstname }} {{ result.surname }}
        </Heading>
        <Text>
          {{ result.position }}
        </Text>
      </div>
    </div>
    <Keywords
      v-if="result.keywords"
      :keywords="keywordsStringToArray(result.keywords)"
    />
    <CollapseSection collapse-title="About">
      <Text class="break-words break-all whitespace-pre-wrap">
        {{ result.about }}
      </Text>
    </CollapseSection>
    <CollapseSection collapse-title="Publications & Research">
      <Card
        v-for="research in relatedResearch"
        :key="research.id"
        button-title="Learn more"
        :card-image="ResearchBanner"
        card-image-alt="Research Paper Banner"
        :card-title="research.name"
        :card-text="research.summary"
        :link="'/research/' + research.id.toString()"
      />
    </CollapseSection>
    <div class="flex flex-col gap-[var(--spacing-in-sections)]">
      <Heading heading="h3"> Let's connect! </Heading>
      <div class="flex flex-col">
        <Text>AI Lab</Text>
        <Text>Office 2.01</Text>
      </div>
      <div class="w-full flex gap-[var(--spacing-in-sections)]">
        <a
          v-if="result.email"
          class="btn btn-secondary flex-grow"
          :href="'mailto:' + result.email"
        >
          <Text button>Contact via E-Mail</Text>
        </a>
        <a
          v-if="result.linkedIn"
          class="btn btn-outline btn-secondary"
          :href="result.linkedIn"
          target="_blank"
        >
          LinkedIn
        </a>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { useRoute } from "vue-router";
import Header from "../components/Header.vue";
import { ref, watch } from "vue";
import type { Research, Researchers } from "../types/types.ts";
import { useApiFetch } from "../api/useApiFetch.ts";
import Avatar from "../components/Avatar.vue";
import Heading from "../components/Heading.vue";
import Keywords from "../components/Keywords.vue";
import CollapseSection from "../components/CollapseSection.vue";
import Card from "../components/Card.vue";
import Text from "../components/Text.vue";
import ResearchBanner from "../assets/img/research-paper-banner-ai.png";
import { keywordsStringToArray } from "../utils/helpers.ts";

const route = useRoute();
const id = route.params.id;

const result = ref<Researchers>({
  id: 0,
  firstname: "",
  surname: "",
  related_research: 0,
});

const relatedResearch = ref<Research[]>([]);

const { data: researchersData } = useApiFetch<Researchers>("researchers/" + id);
const { data: researchData } = useApiFetch<Research[]>("research");

watch(researchersData, () => {
  if (researchersData.value) {
    result.value = researchersData.value;
  }
});

watch(researchData, () => {
  if (researchData.value) {
    relatedResearch.value = researchData.value.filter(
      (research) =>
        Array.isArray(result.value.related_research) &&
        research.id === Number(id),
    );
  }
});

const keywords = ["Keyword 1", "Keyword 2", "Keyword 3"];
</script>
