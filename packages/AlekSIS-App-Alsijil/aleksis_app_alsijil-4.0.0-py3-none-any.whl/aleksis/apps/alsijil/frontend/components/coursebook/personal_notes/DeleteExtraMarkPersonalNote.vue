<script>
import { deletePersonalNotes } from "./personal_notes.graphql";
import ConfirmDialog from "aleksis.core/components/generic/dialogs/ConfirmDialog.vue";
import mutateMixin from "aleksis.core/mixins/mutateMixin.js";
import personalNoteRelatedMixin from "./personalNoteRelatedMixin";

export default {
  name: "DeleteAssignedExtraMark",
  components: {
    ConfirmDialog,
  },
  mixins: [mutateMixin, personalNoteRelatedMixin],
  props: {
    personalNote: {
      type: Object,
      required: true,
    },
    person: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      showDeleteConfirm: false,
    };
  },
  methods: {
    deleteNote() {
      this.mutate(
        deletePersonalNotes,
        {
          ids: [this.personalNote.id],
        },
        (storedPersonalNotes) => {
          const index = storedPersonalNotes.findIndex(
            (n) => n.id === this.personalNote.id,
          );
          storedPersonalNotes.splice(index, 1);

          return storedPersonalNotes;
        },
      );
    },
  },
};
</script>

<template>
  <v-btn color="error" icon @click.prevent.stop="showDeleteConfirm = true">
    <v-icon color="error">$deleteContent</v-icon>
    <confirm-dialog
      v-model="showDeleteConfirm"
      @confirm="deleteNote"
      @cancel="showDeleteConfirm = false"
    >
      <template #title>
        {{ $t("alsijil.personal_notes.confirm_delete") }}
      </template>
      <template #text>
        {{
          $t("alsijil.personal_notes.confirm_delete_extra_mark", {
            extraMark: personalNote.extraMark.name,
            name: person.firstName || person.fullName,
          })
        }}
      </template>
    </confirm-dialog>
  </v-btn>
</template>
