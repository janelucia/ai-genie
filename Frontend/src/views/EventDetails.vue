<template>
  <PageStructure>
    <div class="flex flex-col gap-[var(--spacing-in-sections)] w-full">
      <Heading heading="h1" class="text-center">
        {{ result.name }}
      </Heading>
      <Picture
        :image="EventBanner"
        image-alt="Event banner"
        picture-class="rounded"
      />
    </div>
    <div class="flex flex-col gap-[var(--spacing-in-sections)]">
      <div class="flex gap-[var(--spacing-in-sections)] justify-between w-full">
        <div class="flex gap-[var(--spacing-in-sections)] w-1/2">
          <Text>🗓️</Text>
          <div>
            <Text class="whitespace-nowrap"> {{ formattedDate.date }}, </Text>
            <Text class="whitespace-nowrap">
              {{ formattedDate.time }}
            </Text>
          </div>
        </div>
        <div
          v-if="result.location"
          class="flex gap-[var(--spacing-in-sections)] w-1/2"
        >
          <Text>📍</Text>
          <div class="flex flex-col">
            <Text v-for="addressLine in stringToArray(result.location)">
              {{ addressLine }}
            </Text>
          </div>
        </div>
      </div>
      <Text>
        {{ result.description }}
      </Text>
    </div>
    <fieldset
      class="fieldset w-full bg-base-200 border border-base-300 p-4 rounded-box"
    >
      <legend class="fieldset-legend">
        <Heading heading="h2"> Sign Up </Heading>
      </legend>

      <label class="fieldset-label">
        <Text small> Name </Text>
      </label>
      <input
        v-model="name"
        type="text"
        class="input w-full"
        placeholder="Name"
        @blur="updateSignature('name')"
        :class="{
          'input-error': nameTouched && !name,
          'input-success': nameTouched && name,
        }"
      />

      <label class="fieldset-label">
        <Text small> Email </Text>
      </label>
      <input
        v-model="email"
        type="email"
        class="input w-full"
        :class="{
          'input-error': emailTouched && email && !isValidEmail,
          'input-success': emailTouched && email && isValidEmail,
        }"
        placeholder="Email"
        @blur="updateSignature('email')"
      />

      <Text
        v-if="emailTouched && email && !isValidEmail"
        class="text-error mt-1"
        small
      >
        Please enter a valid email address.
      </Text>

      <label class="fieldset-label">
        <Text small> Message </Text>
      </label>
      <textarea
        v-model="message"
        class="textarea w-full"
        placeholder="Message"
      ></textarea>

      <div
        class="w-full flex items-center gap-[var(--spacing-in-sections)] pt-[var(--spacing-in-sections)]"
      >
        <button
          class="btn"
          :class="[
            submitted || isUserSignedUp(id)
              ? 'btn-disabled bg-gray-400 border-gray-400 cursor-not-allowed flex-grow'
              : !isValidEmail || !name || !message
                ? 'btn-disabled opacity-50 cursor-not-allowed w-full'
                : 'btn-primary w-full',
          ]"
          :disabled="
            submitted ||
            !isValidEmail ||
            !name ||
            !message ||
            isUserSignedUp(id)
          "
          @click="handleSubmit"
        >
          {{
            submitted || isUserSignedUp(id) ? "Already Signed Up" : "Sign Up"
          }}
        </button>
        <button
          v-if="submitted || isUserSignedUp(id)"
          class="btn btn-secondary"
          @click="exportToICS(result.name, result.date)"
        >
          <Text button>Export ICS</Text>
        </button>
      </div>
    </fieldset>
    <Alert
      v-if="showConfirmation"
      class="toast toast-top z-10"
      alert-type="success"
    >
      <Text class="text-wrap">
        You have successfully signed up for the event!
      </Text>
    </Alert>
    <div class="flex flex-col gap-[var(--spacing-in-sections)] w-full">
      <Heading heading="h2"> Event Organizer </Heading>
      <Text class="whitespace-break-spaces overflow-hidden">
        Organizer: {{ result.contact_email }}
      </Text>
    </div>
  </PageStructure>
</template>

<script setup lang="ts">
import { useRoute } from "vue-router";
import { $fetch, useApiData } from "../api/useApiRequest.ts";
import { computed, onMounted, ref, watch } from "vue";
import type { Email, Events } from "../types/types.ts";
import Heading from "../components/Heading.vue";
import Text from "../components/Text.vue";
import { formatDate, formatTime } from "../utils/dateUtils.ts";
import Alert from "../components/Alert.vue";
import Picture from "../components/Picture.vue";
import EventBanner from "/img/event-banner-ai.png";
import { format } from "date-fns";
import PageStructure from "../components/PageStructure.vue";
import {
  isUserSignedUp,
  signUpForEvent,
  stringToArray,
} from "../utils/helpers.ts";

const route = useRoute();
const id = Array.isArray(route.params.id)
  ? route.params.id[0]
  : route.params.id;

const result = ref<Events>({
  id: 0,
  name: "",
  date: "",
  description: "",
  contact_email: "",
  location: "",
});
const name = ref("");
const email = ref("");
const message = ref("Hi, I'd like to sign up for this event.");
const messageWithSignature = ref("Hi, I'd like to sign up for this event.");
const submitted = ref(false);
const emailTouched = ref(false);
const nameTouched = ref(false);
const showConfirmation = ref(false);

const { data } = useApiData<Events>("events/" + id);

const formattedDate = computed(() => {
  if (result.value.date) {
    const date = formatDate(result.value.date);
    const time = formatTime(result.value.date);
    return {
      date,
      time,
    };
  }
  return { date: "", time: "" };
});

/**
 * Adds additional information to the email for the organizer, without displaying it to the user.
 * @param kind
 */
function updateSignature(kind: "email" | "name") {
  if (kind === "email") {
    emailTouched.value = true;
  } else if (kind === "name") {
    nameTouched.value = true;
  }
  messageWithSignature.value = messageWithSignature.value.replace(
    /\n\nName: .+\nEmail: .+/,
    "",
  );

  if (name.value && isValidEmail.value) {
    messageWithSignature.value =
      messageWithSignature.value.trim() +
      `\n\nName: ${name.value}\nEmail: ${email.value}`;
  }
  console.log(messageWithSignature.value);
}

const isValidEmail = computed(() =>
  /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value),
);

async function handleSubmit() {
  if (!name.value || !email.value || !message.value) {
    alert("Please fill out all fields.");
    return;
  }

  console.log("Sending email to organizer...");
  console.log("From:", email.value);
  console.log("Message:", message.value);
  console.log("messageWithSignature:", messageWithSignature.value);

  await $fetch("email/", "POST", <Email>{
    address: data.value?.contact_email || "ai.genie.signup.system@gmail.com",
    message: messageWithSignature.value,
    subject: `Sign up for event "${result.value.name}"`,
  });

  signUpForEvent(id);
  submitted.value = true;

  showConfirmation.value = true;
  setTimeout(() => (showConfirmation.value = false), 4000);
}

/**
 * Creates a .ics file and triggers a download. It does not take the timezone into account, as the
 * user is most likely in the same timezone as the event (Norway). However, this has to be adjusted
 * if this should change.
 * @param eventTitle
 * @param eventStart
 * @param eventEnd
 */
function exportToICS(
  eventTitle: string,
  eventStart: string,
  eventEnd?: string,
) {
  const dtStart = format(new Date(eventStart), "yyyyMMdd'T'HHmmss");
  const dtEnd = format(new Date(eventEnd || eventStart), "yyyyMMdd'T'HHmmss");

  const icsContent = `BEGIN:VCALENDAR\nVERSION:2.0\nBEGIN:VEVENT\nSUMMARY:${eventTitle}\nDTSTART:${dtStart}\nDTEND:${dtEnd}\nEND:VEVENT\nEND:VCALENDAR`;

  const blob = new Blob([icsContent], { type: "text/calendar;charset=utf-8" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = `${eventTitle.replace(/\s+/g, "_")}.ics`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

onMounted(() => {
  // used as the page focussed on the input fields and should start at the top of the page
  window.scrollTo(0, 0);
  isUserSignedUp(id);
});

watch(data, () => {
  if (data.value) {
    result.value = data.value;
    message.value = `Hi, I\'d like to sign up for the event "${result.value.name}" on ${formattedDate.value.date} at ${formattedDate.value.time}.`;
    messageWithSignature.value = message.value;
  }
});
</script>
