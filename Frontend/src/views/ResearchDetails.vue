<template>
  <PageStructure>
    <PictureWithToolTip
      :image="ResearchBanner"
      image-alt="ResearchBanner"
      tooltip-text="This image was created using AI and has no relation to the research."
      picture-class="rounded"
    />
    <div
      v-if="data?.researchers_related?.length"
      class="carousel overflow-x-auto max-w-full px-4 space-x-4"
    >
      <div
        v-for="researcher in data.researchers_related"
        :key="researcher.id"
        class="carousel-item w-24 shrink-0 flex flex-col items-center relative"
      >
        <button @click="router.push(`/researchers/${researcher.id}`)">
          <Avatar class="w-24" />
        </button>
        <Text
          small
          class="text-center badge badge-secondary h-fit absolute bottom-0 w-full"
        >
          {{ researcher.firstname }} {{ researcher.surname }}
        </Text>
      </div>
    </div>
    <Text class="w-full">{{ data?.summary }}</Text>
    <Keywords
      v-if="data?.keywords"
      :keywords="keywordsStringToArray(data.keywords)"
    />
    <a
      :href="'http://localhost:8000' + data?.source_file"
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
import { useApiFetch } from "../api/useApiFetch.ts";
import Text from "../components/Text.vue";
import type { Research } from "../types/types.ts";
import router from "../router";
import Avatar from "../components/Avatar.vue";
import Keywords from "../components/Keywords.vue";
import PictureWithToolTip from "../components/PictureWithToolTip.vue";
import ResearchBanner from "../assets/img/research-paper-banner-ai.png";
import { keywordsStringToArray } from "../utils/helpers.ts";
import PageStructure from "../components/PageStructure.vue";

const route = useRoute();
const id = route.params.id;

const { data } = useApiFetch<Research>("research/" + id);
</script>
