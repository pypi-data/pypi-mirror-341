from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

import django_tables2 as tables
from django_tables2.utils import A


class GroupRoleTable(tables.Table):
    class Meta:
        attrs = {"class": "highlight"}

    name = tables.LinkColumn("edit_excuse_type", args=[A("id")])
    edit = tables.LinkColumn(
        "edit_group_role",
        args=[A("id")],
        text=_("Edit"),
        attrs={"a": {"class": "btn-flat waves-effect waves-orange orange-text"}},
    )
    delete = tables.LinkColumn(
        "delete_group_role",
        args=[A("id")],
        text=_("Delete"),
        attrs={"a": {"class": "btn-flat waves-effect waves-red red-text"}},
    )

    def render_name(self, value, record):
        context = dict(role=record)
        return render_to_string("alsijil/group_role/chip.html", context)

    def before_render(self, request):
        if not request.user.has_perm("alsijil.edit_grouprole_rule"):
            self.columns.hide("edit")
        if not request.user.has_perm("alsijil.delete_grouprole_rule"):
            self.columns.hide("delete")
