<template>
  <PageStructure no-back>
    <div class="w-full flex justify-center">
      <video autoplay loop src="/video/waving-pepper.mp4" class="w-1/2" />
    </div>
    <Heading heading="h1" class="">Welcome @ AI Lab</Heading>
    <div class="flex flex-col gap-[var(--spacing-in-sections)]">
      <Heading heading="h2"> Whats new? </Heading>
      <Alert class="alert-dash" alert-type="info">
        <div class="flex flex-col gap-[var(--spacing-in-sections)]">
          <Text>
            We have our own chat bot for all your questions regarding the AI
            Lab. Have fun exploring!
          </Text>
          <router-link to="/chat">
            <button class="btn btn-secondary w-full">Try it out!</button>
          </router-link>
        </div>
      </Alert>
    </div>
    <div class="flex flex-col gap-[var(--spacing-in-sections)]">
      <Heading heading="h2"> Upcoming Events </Heading>

      <CardCarousel
        :items="eventsResult"
        :banner-image="EventBanner"
        banner-image-alt="Event Banner"
        placeholder-text="This is a placeholder text for the event description. It should be replaced with the actual event description."
        link="/events/"
        vertical
        event
      />
    </div>
    <div class="flex flex-col gap-[var(--spacing-in-sections)]">
      <Heading heading="h2"> Research Highlights </Heading>
      <CardCarousel
        :items="researchResult"
        :banner-image="ResearchBanner"
        banner-image-alt="Research Banner"
        link="/research/"
      />
    </div>
  </PageStructure>
</template>

<script setup lang="ts">
import Heading from "../components/Heading.vue";
import { ref, watch } from "vue";
import type { Research, Events, CardType } from "../types/types.ts";
import { useApiData } from "../api/useApiRequest.ts";
import EventBanner from "/img/event-banner-ai.png";
import ResearchBanner from "/img/research-paper-banner-ai.png";
import Alert from "../components/Alert.vue";
import Text from "../components/Text.vue";
import CardCarousel from "../components/CardCarousel.vue";
import PageStructure from "../components/PageStructure.vue";

const researchResult = ref<CardType[]>([]);
const eventsResult = ref<CardType[]>([]);

const { data: researchData } = useApiData<Research[]>("research");
const { data: eventsData } = useApiData<Events[]>("events");

watch(researchData, () => {
  if (researchData.value) {
    researchResult.value = researchData.value
      .filter(
        (item): item is Research & { id: number } => item.id !== undefined,
      )
      .slice(0, 3)
      .map((item) => {
        return {
          id: item.id,
          name: item.name,
          description: item.summary ?? "",
        };
      });
  }
});

watch(eventsData, () => {
  if (eventsData.value) {
    eventsResult.value = eventsData.value
      .filter((item): item is Events & { id: number } => item.id !== undefined)
      .slice(0, 3)
      .map((item) => {
        return {
          id: item.id,
          name: item.name,
          date: item.date,
          description: item.description,
        };
      });
  }
});
</script>
