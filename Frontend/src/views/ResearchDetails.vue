<template>
  <PageStructure>
    <Heading heading="h1" class="text-center">
      {{ data?.name }}
    </Heading>
    <Picture
      :image="ResearchBanner"
      image-alt="ResearchBanner"
      picture-class="rounded"
    />
    <div
      v-if="data?.researchers_related?.length"
      class="carousel overflow-x-auto max-w-full px-4 space-x-4"
    >
      <button
        v-for="researcher in data.researchers_related"
        :key="researcher.id"
        class="carousel-item w-24 shrink-0 flex flex-col items-center relative"
        @click="router.push(`/researchers/${researcher.id}`)"
      >
        <Avatar
          class="w-24 h-24"
          :img="
            researcher.img ? baseUrl + researcher.img : ResearcherPlaceholder
          "
          :name="researcher.firstname + ' ' + researcher.surname"
        />
        <Text
          small
          class="text-center badge badge-secondary h-fit absolute bottom-0 w-full line-clamp-2"
        >
          {{ researcher.firstname }}
        </Text>
      </button>
    </div>
    <Text v-if="data?.summary" class="w-full">{{ data?.summary }}</Text>
    <Keywords
      v-if="data?.keywords"
      :keywords="stringToArray(data.keywords)"
      link="/research?keywords="
    />
    <button class="btn btn-primary w-full" @click="openChat">
      <Text button>Ask AIGenie</Text>
    </button>
    <a
      v-if="data?.source_file"
      :href="baseUrl + data?.source_file"
      download
      target="_blank"
      class="btn btn-secondary text-base-100 w-full"
    >
      Download Paper
    </a>
  </PageStructure>
</template>

<script setup lang="ts">
import { useRoute } from "vue-router";
import { useApiData } from "../api/useApiRequest.ts";
import Text from "../components/Text.vue";
import type { Research } from "../types/types.ts";
import router from "../router";
import Avatar from "../components/Avatar.vue";
import Keywords from "../components/Keywords.vue";
import Picture from "../components/Picture.vue";
import ResearchBanner from "/img/research-paper-banner-ai.png";
import PageStructure from "../components/PageStructure.vue";
import ResearcherPlaceholder from "/img/placeholder-researcher.png";
import Heading from "../components/Heading.vue";
import { stringToArray } from "../utils/helpers.ts";

const route = useRoute();
const id = route.params.id;
const baseUrl = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const { data } = useApiData<Research>("research/" + id);

/**
 * Function which opens the chat with a prompt to simplify the way to get more information about the research paper.
 */
function openChat() {
  const message = `Hello, I am interested in the research paper titled "${data?.value?.name}". Can you provide me with more information?`;
  localStorage.setItem("chat-message-research", message);
  router.push("/chat");
}
</script>
