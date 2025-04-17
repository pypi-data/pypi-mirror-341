<script>
import AbsenceReasonButtons from "aleksis.apps.kolego/components/AbsenceReasonButtons.vue";
import updateParticipationMixin from "./updateParticipationMixin";

export default {
  name: "UpdateParticipations",
  components: {
    AbsenceReasonButtons,
  },
  mixins: [updateParticipationMixin],
  props: {
    participationStatuses: {
      type: Array,
      required: true,
    },
    absenceReasons: {
      type: Array,
      required: true,
    },
  },
  emits: ["update:participationStatuses"],
  methods: {
    afterSendToServer() {
      this.$once("save", () => this.$emit("update:participationStatuses", []));
    },
  },
};
</script>

<template>
  <v-card>
    <v-card-text>
      <h4>{{ $t("alsijil.coursebook.participation_status") }}</h4>
      <absence-reason-buttons
        allow-empty
        empty-value="present"
        :custom-absence-reasons="absenceReasons"
        @input="sendToServer(participationStatuses, 'absenceReason', $event)"
      />
    </v-card-text>
  </v-card>
</template>

<style scoped></style>
