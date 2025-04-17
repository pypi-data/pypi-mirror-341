<template>
  <statistics-for-person-card v-bind="{ ...$attrs, ...$props }">
    <template #header>
      <base-button
        :icon="true"
        icon-text="mdi-open-in-new"
        i18n-key=""
        :to="{
          name: $route.name,
          params: $route.params,
          hash: '#' + MODE.PARTICIPATIONS,
        }"
      />
      <statistics-for-person-page
        v-if="Object.values(MODE).includes(mode)"
        :person-id="person.id"
      />
    </template>
  </statistics-for-person-card>
</template>

<script>
import personOverviewCardMixin from "aleksis.core/mixins/personOverviewCardMixin.js";
import BaseButton from "aleksis.core/components/generic/buttons/BaseButton.vue";
import StatisticsForPersonPage from "./StatisticsForPersonPage.vue";
import StatisticsForPersonCard from "./StatisticsForPersonCard.vue";

import { MODE } from "./modes";

export default {
  name: "StatisticsForPersonWidget",
  mixins: [personOverviewCardMixin],
  components: {
    BaseButton,
    StatisticsForPersonPage,
    StatisticsForPersonCard,
  },
  computed: {
    MODE() {
      return MODE;
    },
    mode() {
      return this.$hash;
    },
  },
};
</script>
