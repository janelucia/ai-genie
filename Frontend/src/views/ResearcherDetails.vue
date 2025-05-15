<template>
  <PageStructure>
    <div
      class="flex items-center justify-evenly w-full gap-[var(--spacing-in-sections)]"
    >
      <Avatar
        class="w-32 h-32"
        :img="data?.img ? baseUrl + data.img : ResearcherPlaceholder"
        :name="data?.firstname + ' ' + data?.surname"
      />
      <div class="w-1/2">
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
      :keywords="stringToArray(data?.keywords)"
      link="/researchers?keywords="
    />
    <CollapseSection v-if="data?.about" collapse-title="About">
      <Text>
        {{ data?.about }}
      </Text>
    </CollapseSection>
    <CollapseSection
      v-if="relatedResearch.length > 0"
      collapse-title="Publications & Research"
    >
      <Card
        v-for="research in relatedResearch"
        :key="research.id"
        button-title="Learn more"
        :card-image="ResearchBanner"
        card-image-alt="Research Paper Banner"
        :card-title="research.name"
        :card-text="research.summary"
        :link="'/research/' + research.id?.toString()"
      />
    </CollapseSection>
    <div
      v-if="data?.office || data?.email || data?.linkedin"
      class="flex flex-col gap-[var(--spacing-in-sections)]"
    >
      <Heading heading="h3"> Let's connect! </Heading>
      <div v-if="data?.office" class="flex flex-col">
        <Text v-for="addressLine of stringToArray(data.office)">{{
          addressLine
        }}</Text>
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
          v-if="data?.linkedin"
          class="btn btn-outline btn-secondary"
          :href="data?.linkedin"
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
import { stringToArray } from "../utils/helpers.ts";
import PageStructure from "../components/PageStructure.vue";
import ResearcherPlaceholder from "/img/placeholder-researcher.png";

const route = useRoute();
const id = route.params.id;
const baseUrl = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

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
