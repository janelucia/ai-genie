<template>
  <PageStructure>
    <div
      class="flex items-center justify-evenly w-full gap-[var(--spacing-in-sections)]"
    >
      <Avatar class="w-32" />
      <div>
        <Heading heading="h1">
          {{ data?.firstname }} {{ data?.surname }}
        </Heading>
        <Text>
          {{ data?.position }}
        </Text>
      </div>
    </div>
    <Keywords
      v-if="data?.keywords"
      :keywords="keywordsStringToArray(data?.keywords)"
    />
    <CollapseSection collapse-title="About">
      <Text class="break-words break-all whitespace-pre-wrap">
        {{ data?.about }}
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
          v-if="data?.email"
          class="btn btn-secondary flex-grow"
          :href="'mailto:' + data?.email"
        >
          <Text button>Contact via E-Mail</Text>
        </a>
        <a
          v-if="data?.linkedIn"
          class="btn btn-outline btn-secondary"
          :href="data?.linkedIn"
          target="_blank"
        >
          LinkedIn
        </a>
      </div>
    </div>
  </PageStructure>
</template>
<script setup lang="ts">
import { useRoute } from "vue-router";
import { ref, watch } from "vue";
import type { Research, Researchers } from "../types/types.ts";
import { useApiRequest } from "../api/useApiRequest.ts";
import Avatar from "../components/Avatar.vue";
import Heading from "../components/Heading.vue";
import Keywords from "../components/Keywords.vue";
import CollapseSection from "../components/CollapseSection.vue";
import Card from "../components/Card.vue";
import Text from "../components/Text.vue";
import ResearchBanner from "/img/research-paper-banner-ai.png";
import { keywordsStringToArray } from "../utils/helpers.ts";
import PageStructure from "../components/PageStructure.vue";

const route = useRoute();
const id = route.params.id;

const relatedResearch = ref<Research[]>([]);

const { data } = useApiRequest<Researchers>("researchers/" + id);
const { data: researchData } = useApiRequest<Research[]>("research");

watch(researchData, () => {
  if (researchData.value) {
    relatedResearch.value = researchData.value.filter(
      (research) =>
        Array.isArray(data?.value?.related_research) &&
        research.id === Number(id),
    );
  }
});
</script>
