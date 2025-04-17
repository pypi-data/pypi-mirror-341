<template>
  <v-form ref="form" @input="$emit('valid', $event)">
    <v-container>
      <v-row>
        <div aria-required="true" class="full-width">
          <!-- FIXME Vue 3: clear-on-select -->
          <person-field
            :gql-query="gqlQuery"
            :label="$t('forms.labels.persons')"
            return-object
            multiple
            chips
            deletable-chips
            :rules="
              $rules().build([
                (value) => value.length > 0 || $t('forms.errors.required'),
              ])
            "
            :value="persons"
            @input="$emit('persons', $event)"
          />
        </div>
      </v-row>
      <v-row>
        <v-col cols="12" :sm="startPeriods ? 4 : 6" class="pl-0">
          <div aria-required="true">
            <date-time-field
              :label="$t('forms.labels.start')"
              :rules="$rules().required.build()"
              :value="start.toISO()"
              @input="handleStartDate"
            />
          </div>
        </v-col>
        <v-col cols="12" :sm="2" v-if="startPeriods" align-self="end">
          <v-select
            :label="$t('lesrooster.slot.period')"
            :items="startPeriods"
            item-text="period"
            :value="startSlot"
            @input="handleStartSlot"
            return-object
          />
        </v-col>
        <v-col cols="12" :sm="endPeriods ? 4 : 6" class="pr-0">
          <div aria-required="true">
            <date-time-field
              :label="$t('forms.labels.end')"
              :rules="$rules().required.build()"
              :value="end.toISO()"
              @input="handleEndDate"
            />
          </div>
        </v-col>
        <v-col cols="12" :sm="2" v-if="endPeriods" align-self="end">
          <v-select
            :label="$t('lesrooster.slot.period')"
            :items="endPeriods"
            item-text="period"
            :value="endSlot"
            @input="handleEndSlot"
            return-object
          />
        </v-col>
      </v-row>
      <v-row>
        <v-text-field
          :label="$t('forms.labels.comment')"
          :value="comment"
          :disabled="absenceReason == 'present'"
          @input="$emit('comment', $event)"
        />
      </v-row>
      <v-row>
        <div aria-required="true">
          <absence-reason-group-select
            :rules="$rules().required.build()"
            allow-empty
            :value="absenceReason"
            :custom-absence-reasons="absenceReasons"
            @input="$emit('absence-reason', $event)"
          />
        </div>
      </v-row>
    </v-container>
  </v-form>
</template>

<script>
import AbsenceReasonGroupSelect from "aleksis.apps.kolego/components/AbsenceReasonGroupSelect.vue";
import DateTimeField from "aleksis.core/components/generic/forms/DateTimeField.vue";
import PersonField from "aleksis.core/components/generic/forms/PersonField.vue";
import { gqlPersons, periodsByDay } from "./absenceCreation.graphql";
import formRulesMixin from "aleksis.core/mixins/formRulesMixin.js";
import { DateTime } from "luxon";

export default {
  name: "AbsenceCreationForm",
  components: {
    AbsenceReasonGroupSelect,
    DateTimeField,
    PersonField,
  },
  mixins: [formRulesMixin],
  emits: [
    "valid",
    "persons",
    "start-date",
    "end-date",
    "comment",
    "absence-reason",
  ],
  apollo: {
    periodsByDay: {
      query: periodsByDay,
      result(_) {
        this.handleStartDate(this.start.toISO());
        this.handleEndDate(this.end.toISO());
      },
    },
  },
  props: {
    persons: {
      type: Array,
      required: true,
    },
    startDate: {
      type: String,
      required: true,
    },
    endDate: {
      type: String,
      required: true,
    },
    comment: {
      type: String,
      required: true,
    },
    absenceReason: {
      type: String,
      required: true,
    },
    absenceReasons: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      gqlQuery: gqlPersons,
      startDT: DateTime.fromISO(this.startDate),
      endDT: DateTime.fromISO(this.endDate),
      startPeriods: false,
      endPeriods: false,
      startSlot: undefined,
      endSlot: undefined,
    };
  },
  computed: {
    start: {
      get() {
        return this.startDT;
      },
      set(dt) {
        this.startDT = dt;
        if (dt >= this.end) {
          this.end = dt.plus({ minutes: 5 });
        }
        this.$emit("start-date", dt.toISO());
      },
    },
    end: {
      get() {
        return this.endDT;
      },
      set(dt) {
        this.endDT = dt;
        if (dt <= this.start) {
          this.start = dt.minus({ minutes: 5 });
        }
        this.$emit("end-date", dt.toISO());
      },
    },
  },
  methods: {
    getPeriodsForWeekday(weekday) {
      // Adapt from python conventions
      const pythonWeekday = weekday - 1;
      let periodsForWeekday = this.periodsByDay.find(
        (period) => period.weekday === pythonWeekday,
      );
      if (!periodsForWeekday) return false;
      return periodsForWeekday.periods;
    },
    handleStartDate(date) {
      this.start = DateTime.fromISO(date);

      if (this.periodsByDay && this.periodsByDay.length > 0) {
        // Select periods for day
        this.startPeriods = this.getPeriodsForWeekday(this.start.weekday);
        if (!this.startPeriods) return;
        // Sync PeriodSelect
        const startTime = this.start.toFormat("HH:mm:ss");
        this.startSlot = this.startPeriods.find(
          (period) => period.timeStart === startTime,
        );
      }
    },
    handleEndDate(date) {
      this.end = DateTime.fromISO(date);

      if (this.periodsByDay && this.periodsByDay.length > 0) {
        // Select periods for day
        this.endPeriods = this.getPeriodsForWeekday(this.end.weekday);
        if (!this.endPeriods) return;
        // Sync PeriodSelect
        const endTime = this.end.toFormat("HH:mm:ss");
        this.endSlot = this.endPeriods.find(
          (period) => period.endTime === endTime,
        );
      }
    },
    handleStartSlot(slot) {
      // Sync TimeSelect
      const startTime = DateTime.fromISO(slot.timeStart);
      this.start = this.start.set({
        hour: startTime.hour,
        minute: startTime.minute,
        second: startTime.second,
      });
    },
    handleEndSlot(slot) {
      // Sync TimeSelect
      const endTime = DateTime.fromISO(slot.timeEnd);
      this.end = this.end.set({
        hour: endTime.hour,
        minute: endTime.minute,
        second: endTime.second,
      });
    },
  },
};
</script>
