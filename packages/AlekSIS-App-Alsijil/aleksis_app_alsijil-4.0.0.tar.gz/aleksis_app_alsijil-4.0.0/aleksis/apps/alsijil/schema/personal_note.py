from graphene_django import DjangoObjectType

from aleksis.apps.alsijil.models import PersonalNote
from aleksis.core.schema.base import (
    BaseBatchCreateMutation,
    BaseBatchDeleteMutation,
    BaseBatchPatchMutation,
    DjangoFilterMixin,
    OptimisticResponseTypeMixin,
    PermissionsTypeMixin,
)


class PersonalNoteType(
    OptimisticResponseTypeMixin,
    PermissionsTypeMixin,
    DjangoFilterMixin,
    DjangoObjectType,
):
    class Meta:
        model = PersonalNote
        fields = (
            "id",
            "note",
            "extra_mark",
            "documentation",
        )

    @staticmethod
    def resolve_can_edit(root: PersonalNote, info, **kwargs):
        return info.context.user.has_perm("alsijil.edit_personal_note_rule", root)

    @staticmethod
    def resolve_can_delete(root: PersonalNote, info, **kwargs):
        return info.context.user.has_perm("alsijil.edit_personal_note_rule", root)


class PersonalNoteBatchCreateMutation(BaseBatchCreateMutation):
    class Meta:
        model = PersonalNote
        type_name = "BatchCreatePersonalNoteInput"
        return_field_name = "personalNotes"
        fields = ("note", "extra_mark", "documentation", "person")
        permissions = ("alsijil.edit_personal_note_rule",)


class PersonalNoteBatchPatchMutation(BaseBatchPatchMutation):
    class Meta:
        model = PersonalNote
        type_name = "BatchPatchPersonalNoteInput"
        return_field_name = "personalNotes"
        fields = ("id", "note", "extra_mark", "documentation", "person")
        permissions = ("alsijil.edit_personal_note_rule",)


class PersonalNoteBatchDeleteMutation(BaseBatchDeleteMutation):
    class Meta:
        model = PersonalNote
        permissions = ("alsijil.edit_personal_note_rule",)
