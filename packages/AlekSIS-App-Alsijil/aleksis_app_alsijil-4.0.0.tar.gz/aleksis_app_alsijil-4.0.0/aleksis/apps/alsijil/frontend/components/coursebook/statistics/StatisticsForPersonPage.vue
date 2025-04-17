<template>
  <fullscreen-dialog-page
    :fallback-url="{ name: 'core.personById', props: { id: personId } }"
  >
    <template #title>
      {{
        $t("alsijil.coursebook.statistics.person_page.title", {
          fullName: personName?.fullName || "???",
        })
      }}
    </template>
    <div class="d-flex" style="gap: 4em">
      <div class="flex-grow-1" style="max-width: 100%">
        <!-- documentations for person list -->
        <c-r-u-d-iterator
          i18n-key="alsijil.coursebook.statistics"
          :gql-query="gqlQuery"
          :gql-additional-query-args="gqlQueryArgs"
          :enable-create="false"
          :enable-edit="false"
          :elevated="false"
          @lastQuery="lastQuery = $event"
        >
          <template #additionalActions>
            <v-btn-toggle
              :value="mode"
              @change="updateMode"
              mandatory
              color="secondary"
              rounded
              dense
            >
              <v-btn outlined :value="MODE.PARTICIPATIONS">
                {{ $t("alsijil.coursebook.absences.absences") }}
              </v-btn>
              <v-btn outlined :value="MODE.PERSONAL_NOTES">
                {{ $t("alsijil.personal_notes.personal_notes") }}
              </v-btn>
            </v-btn-toggle>
            <v-btn
              v-if="$vuetify.breakpoint.mobile"
              rounded
              dense
              outlined
              text
              @click="statisticsBottomSheet = !statisticsBottomSheet"
            >
              {{ $t("alsijil.coursebook.statistics.person_page.summary") }}
            </v-btn>
          </template>
          <template #default="{ items }">
            <v-expand-transition>
              <update-participations
                v-show="selected.length > 0"
                class="mt-2"
                :subjects="[]"
                :absence-reasons="absenceReasons"
                :participation-statuses.sync="selected"
                :extra-marks="[]"
                :affected-query="lastQuery"
                :documentation="{}"
              />
            </v-expand-transition>

            <v-item-group multiple v-model="selected" class="mt-2">
              <v-expansion-panels focusable>
                <v-expansion-panel
                  v-for="item in items"
                  :key="item.id"
                  ripple
                  :readonly="!showEdit(item)"
                >
                  <v-expansion-panel-header
                    :hide-actions="!showEdit(item) && !showDelete(item)"
                    disable-icon-rotate
                  >
                    <template #actions>
                      <v-btn v-if="showEdit(item)" color="primary" icon>
                        <v-icon> $edit </v-icon>
                      </v-btn>
                      <delete-assigned-extra-mark
                        v-if="showDelete(item)"
                        :personal-note="item"
                        :participation="item.participation || {}"
                        :subjects="[]"
                        :absence-reasons="[]"
                        :extra-marks="[]"
                        :affected-query="lastQuery"
                        :documentation="item.relatedDocumentation"
                        :person="personName"
                      />
                    </template>
                    <v-row class="mr-2">
                      <v-col cols="12" md="6" class="pa-0 d-flex">
                        <v-list-item-avatar
                          v-if="
                            mode === MODE.PARTICIPATIONS && showCheckbox(item)
                          "
                        >
                          <v-item v-slot="{ active, toggle }" :value="item.id">
                            <v-simple-checkbox
                              :value="active"
                              @click="toggle"
                            />
                          </v-item>
                        </v-list-item-avatar>
                        <v-list-item-content>
                          <v-list-item-title>
                            <!-- date & timeslot -->
                            <time
                              :datetime="
                                item.relatedDocumentation.datetimeStart
                              "
                              class="text-no-wrap"
                            >
                              {{
                                $d(
                                  $parseISODate(
                                    item.relatedDocumentation.datetimeStart,
                                  ),
                                  "short",
                                )
                              }}
                            </time>

                            <time
                              :datetime="
                                item.relatedDocumentation.datetimeStart
                              "
                              class="text-no-wrap"
                            >
                              {{
                                $d(
                                  $parseISODate(
                                    item.relatedDocumentation.datetimeStart,
                                  ),
                                  "shortTime",
                                )
                              }}
                            </time>
                            <span>-</span>
                            <time
                              :datetime="item.relatedDocumentation.datetimeEnd"
                              class="text-no-wrap"
                            >
                              {{
                                $d(
                                  $parseISODate(
                                    item.relatedDocumentation.datetimeEnd,
                                  ),
                                  "shortTime",
                                )
                              }}
                            </time>
                          </v-list-item-title>
                          <v-list-item-subtitle class="overflow-scroll">
                            <!-- teacher -->
                            <person-chip
                              v-for="teacher in item.relatedDocumentation
                                .teachers"
                              :key="teacher.id"
                              :person="teacher"
                              no-link
                              small
                            />
                            <!-- group -->
                            <span>
                              {{ item.groupShortName }}
                            </span>
                            <!-- subject -->
                            <subject-chip
                              :subject="item.relatedDocumentation.subject"
                              small
                            />
                          </v-list-item-subtitle>
                        </v-list-item-content>
                      </v-col>
                      <v-col cols="12" md="6" class="pa-0">
                        <v-list-item-action
                          class="flex-row full-width justify-md-end ma-0 align-center fill-height"
                        >
                          <v-chip
                            color="warning"
                            class="mx-1"
                            v-if="!item.relatedDocumentation.amended"
                            >{{
                              $t("alsijil.coursebook.statistics.not_counted")
                            }}</v-chip
                          >
                          <!-- chips: absences & extraMarks -->
                          <absence-reason-chip
                            v-if="item.absenceReason"
                            :absence-reason="item.absenceReason"
                          />
                          <tardiness-chip
                            v-if="item.tardiness"
                            :tardiness="item.tardiness"
                            class="ms-1"
                          />
                          <extra-mark-chip
                            v-if="item.extraMark"
                            :extra-mark="item.extraMark"
                          />
                          <personal-note-chip v-if="item.note" :note="item" />
                        </v-list-item-action>
                      </v-col>
                    </v-row>
                  </v-expansion-panel-header>
                  <v-expansion-panel-content>
                    <v-card-text class="pb-0">
                      <text-note
                        v-if="item.note"
                        :value="item"
                        :participation="{}"
                        :person="personName"
                        :subjects="[]"
                        :absence-reasons="absenceReasons"
                        :extra-marks="[]"
                        :affected-query="lastQuery"
                        :documentation="item.relatedDocumentation"
                      />
                      <update-participation
                        v-else
                        :participation="item"
                        :subjects="[]"
                        :absence-reasons="absenceReasons"
                        :extra-marks="[]"
                        :affected-query="lastQuery"
                        :documentation="item.relatedDocumentation"
                      />
                    </v-card-text>
                  </v-expansion-panel-content>
                </v-expansion-panel>
              </v-expansion-panels>
            </v-item-group>
            <v-divider></v-divider>
          </template>
        </c-r-u-d-iterator>
      </div>
      <statistics-for-person-card
        v-if="!$vuetify.breakpoint.mobile"
        class="flex-shrink-1"
        style="min-width: 15vw"
        :compact="false"
        :person="{ id: personId }"
      />
      <v-bottom-sheet v-model="statisticsBottomSheet" v-else>
        <statistics-for-person-card
          :compact="false"
          :person="{ id: personId }"
        />
      </v-bottom-sheet>
    </div>
    <template #actions="{ toolbar }">
      <active-school-term-select
        v-if="toolbar"
        v-model="$root.activeSchoolTerm"
        color="secondary"
      />
      <v-btn
        v-if="toolbar"
        icon
        color="primary"
        :to="{
          name: 'alsijil.coursebookPrintPerson',
          params: { id: personId },
        }"
        target="_blank"
      >
        <v-icon>$print</v-icon>
      </v-btn>
      <FabButton v-else icon-text="$print" i18n-key="actions.print" disabled />
    </template>
  </fullscreen-dialog-page>
</template>

<script>
import { absenceReasons } from "../queries/absenceReasons.graphql";
import AbsenceReasonChip from "aleksis.apps.kolego/components/AbsenceReasonChip.vue";
import ActiveSchoolTermSelect from "aleksis.core/components/school_term/ActiveSchoolTermSelect.vue";
import CRUDIterator from "aleksis.core/components/generic/CRUDIterator.vue";
import FabButton from "aleksis.core/components/generic/buttons/FabButton.vue";
import FullscreenDialogPage from "aleksis.core/components/generic/dialogs/FullscreenDialogPage.vue";
import PersonChip from "aleksis.core/components/person/PersonChip.vue";
import SubjectChip from "aleksis.apps.cursus/components/SubjectChip.vue";
import StatisticsForPersonCard from "./StatisticsForPersonCard.vue";

import {
  participationsOfPerson,
  personalNotesForPerson,
  personName,
} from "./statistics.graphql";
import ExtraMarkChip from "../../extra_marks/ExtraMarkChip.vue";
import { MODE } from "./modes.js";
import PersonalNoteChip from "../personal_notes/PersonalNoteChip.vue";
import TextNote from "../personal_notes/TextNote.vue";
import UpdateParticipation from "../absences/UpdateParticipation.vue";
import TardinessChip from "../absences/TardinessChip.vue";
import DeleteAssignedExtraMark from "../personal_notes/DeleteExtraMarkPersonalNote.vue";
import UpdateParticipations from "../absences/UpdateParticipations.vue";

export default {
  name: "StatisticsForPersonPage",
  components: {
    UpdateParticipations,
    DeleteAssignedExtraMark,
    TardinessChip,
    UpdateParticipation,
    TextNote,
    PersonalNoteChip,
    ActiveSchoolTermSelect,
    ExtraMarkChip,
    AbsenceReasonChip,
    CRUDIterator,
    FabButton,
    FullscreenDialogPage,
    PersonChip,
    SubjectChip,
    StatisticsForPersonCard,
  },
  props: {
    // personId is supplied via the url
    personId: {
      type: [Number, String],
      required: true,
    },
  },
  apollo: {
    personName: {
      query: personName,
      variables() {
        return {
          person: this.personId,
        };
      },
    },
    absenceReasons: {
      query: absenceReasons,
      update: (data) => data.items,
    },
  },
  data() {
    return {
      personName: {},
      statisticsBottomSheet: false,
      lastQuery: null,
      absenceReasons: [],
      selected: [],
    };
  },
  computed: {
    gqlQueryArgs() {
      return {
        person: this.personId,
      };
    },
    MODE() {
      return MODE;
    },
    mode() {
      return this.$hash;
    },
  },
  methods: {
    gqlQuery() {
      return this.mode === MODE.PERSONAL_NOTES
        ? personalNotesForPerson
        : participationsOfPerson;
    },
    updateMode(mode = MODE.PARTICIPATIONS) {
      if (mode === this.mode) {
        return;
      }

      this.selected = [];

      this.$router.replace({
        ...this.$route,
        hash: "#" + mode,
      });
    },
    showEdit(item) {
      // Notes with ExtraMark cannot be edited, only deleted
      return (
        item.canEdit && (item.note || item.absenceReason || item.tardiness)
      );
    },
    showDelete(item) {
      // Only ExtraMarks can be deleted
      return item.canDelete && item.extraMark;
    },
    showCheckbox(item) {
      return this.showEdit(item);
    },
  },
};
</script>
