<template>
  <button v-if="uniqueKeywords.length > 0" class="cursor-pointer" @click="open">
    <img src="../assets/icons/filter.svg" alt="Filter Icon" class="w-7 h-7" />
  </button>
  <dialog ref="modalRef" class="modal">
    <div
      class="modal-box flex flex-col gap-[var(--spacing-in-sections)] max-h-[90vh]"
    >
      <Heading heading="h3"> Filter by Keywords </Heading>

      <div class="flex-1 overflow-y-auto mb-4">
        <div class="flex flex-col gap-2">
          <label
            v-for="keyword in uniqueKeywords"
            :key="keyword"
            class="flex items-center justify-between gap-2 cursor-pointer"
          >
            <Text class="text-wrap">{{ keyword }}</Text>
            <input
              type="checkbox"
              :value="keyword"
              :checked="localSelectedKeywords.includes(keyword)"
              @change="toggleKeyword(keyword)"
              class="checkbox checkbox-secondary"
            />
          </label>
        </div>
      </div>
      <div class="modal-action">
        <button class="btn btn-primary" @click="applyFilter">Apply</button>
        <button class="btn btn-ghost" @click="close">Cancel</button>
      </div>
    </div>
  </dialog>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import Heading from "./Heading.vue";
import Text from "./Text.vue";

const props = defineProps<{
  keywords: string[];
  selectedKeywords: string[];
}>();

const emit = defineEmits<{
  (e: "filter", keywords: string[]): void;
}>();

const modalRef = ref<HTMLDialogElement | null>(null);
const localSelectedKeywords = ref<string[]>([]);

const uniqueKeywords = computed(() => {
  const keywords = props.keywords
    .flatMap((k) => k.split(","))
    .map((k) => k.trim());

  return Array.from(new Set(keywords)).sort();
});

function toggleKeyword(keyword: string) {
  if (localSelectedKeywords.value.includes(keyword)) {
    localSelectedKeywords.value = localSelectedKeywords.value.filter(
      (k) => k !== keyword,
    );
  } else {
    localSelectedKeywords.value.push(keyword);
  }
}

function applyFilter() {
  emit("filter", localSelectedKeywords.value);
  close();
}

function open() {
  localSelectedKeywords.value = [...props.selectedKeywords];
  modalRef.value?.showModal();
}

function close() {
  modalRef.value?.close();
}

defineExpose({ open });
</script>
