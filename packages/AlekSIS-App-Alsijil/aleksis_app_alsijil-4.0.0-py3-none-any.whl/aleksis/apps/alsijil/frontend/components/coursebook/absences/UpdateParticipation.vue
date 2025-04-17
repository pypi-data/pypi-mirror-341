<template>
  <div>
    <absence-reason-group-select
      class="mb-2"
      allow-empty
      :load-selected-chip="loadingIndicator"
      :value="participation.absenceReason?.id || 'present'"
      :custom-absence-reasons="absenceReasons"
      @input="sendToServer([participation], 'absenceReason', $event)"
    />
    <tardiness-field
      v-bind="documentationPartProps"
      :loading="loadingIndicator"
      :disabled="loadingIndicator"
      :participations="[participation]"
      :value="participation.tardiness"
      @input="sendToServer([participation], 'tardiness', $event)"
    />
  </div>
</template>
<script>
import AbsenceReasonGroupSelect from "aleksis.apps.kolego/components/AbsenceReasonGroupSelect.vue";
import TardinessField from "./TardinessField.vue";
import updateParticipationMixin from "./updateParticipationMixin";

export default {
  name: "UpdateParticipation",
  mixins: [updateParticipationMixin],
  components: { AbsenceReasonGroupSelect, TardinessField },
  props: {
    participation: {
      type: Object,
      required: true,
    },
    forceLoading: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  emits: ["beforeSendToServer", "duringSendToServer", "afterSendToServer"],
  methods: {
    beforeSendToServer() {
      this.$emit("beforeSendToServer");
    },
    duringUpdateSendToServer(participations, field, value, incomingStatuses) {
      this.$emit(
        "duringSendToServer",
        participations,
        field,
        value,
        incomingStatuses,
      );
    },
    afterSendToServer(participations, field, value) {
      this.$emit("afterSendToServer", participations, field, value);
    },
  },
  computed: {
    loadingIndicator() {
      return this.loading || this.forceLoading;
    },
  },
};
</script>
