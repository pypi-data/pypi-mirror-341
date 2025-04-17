from datetime import date
from typing import Optional

from django.db.models import Prefetch, Q
from django.utils.translation import gettext as _

from celery.result import allow_join_result
from celery.states import SUCCESS

from aleksis.apps.cursus.models import Course
from aleksis.apps.kolego.models.absence import AbsenceReason
from aleksis.core.models import Group, PDFFile, Person, SchoolTerm
from aleksis.core.util.celery_progress import ProgressRecorder, recorded_task
from aleksis.core.util.pdf import generate_pdf_from_template

from .models import Documentation, ExtraMark, ParticipationStatus, PersonalNote
from .util.statistics import StatisticsBuilder


class PDFGenerationError(Exception):
    """Error in PDF generation."""


@recorded_task
def generate_groups_register_printout(
    groups: list[int],
    file_object: int,
    recorder: ProgressRecorder,
    include_cover: Optional[bool] = True,
    include_abbreviations: Optional[bool] = True,
    include_members_table: Optional[bool] = True,
    include_teachers_and_subjects_table: Optional[bool] = True,
    include_person_overviews: Optional[bool] = True,
    include_coursebook: Optional[bool] = True,
):
    """Generate a configurable register printout as PDF for a group."""

    context = {}

    context["include_cover"] = include_cover
    context["include_abbreviations"] = include_abbreviations
    context["include_members_table"] = include_members_table
    context["include_teachers_and_subjects_table"] = include_teachers_and_subjects_table
    context["include_person_overviews"] = include_person_overviews
    context["include_coursebook"] = include_coursebook

    context["today"] = date.today()

    _number_of_steps = 5 + len(groups)

    recorder.set_progress(1, _number_of_steps, _("Loading data ..."))

    groups = Group.objects.filter(pk__in=groups).order_by("name")

    if include_cover:
        groups = groups.select_related("school_term")

    if include_abbreviations or include_members_table:
        context["absence_reasons"] = AbsenceReason.objects.filter(
            tags__short_name="class_register", count_as_absent=True
        )
        context["absence_reasons_not_counted"] = AbsenceReason.objects.filter(
            tags__short_name="class_register", count_as_absent=False
        )
        context["extra_marks"] = ExtraMark.objects.all()

    if include_members_table or include_person_overviews:
        groups = groups.prefetch_related("members")

    if include_teachers_and_subjects_table:
        groups = groups.prefetch_related(
            Prefetch("courses", queryset=Course.objects.select_related("subject")),
            "courses__teachers",
            "child_groups",
            Prefetch("child_groups__courses", queryset=Course.objects.select_related("subject")),
            "child_groups__courses__teachers",
        )

    recorder.set_progress(2, _number_of_steps, _("Loading groups ..."))

    for i, group in enumerate(groups, start=1):
        recorder.set_progress(
            2 + i, _number_of_steps, _(f"Loading group {group.short_name or group.name} ...")
        )

        if include_members_table or include_person_overviews:
            doc_query_set = Documentation.objects.select_related("subject").prefetch_related(
                "teachers"
            )

            members_with_statistics = (
                StatisticsBuilder(group.members.all()).use_from_group(group).annotate_statistics()
            )
            if include_person_overviews:
                members_with_statistics = members_with_statistics.prefetch_relevant_participations(
                    documentation_with_details=doc_query_set
                ).prefetch_relevant_personal_notes(documentation_with_details=doc_query_set)
            members_with_statistics = members_with_statistics.build()
            group.members_with_stats = members_with_statistics

        if include_teachers_and_subjects_table:
            group.as_list = [group]

        if include_coursebook:
            group.documentations = (
                Documentation.objects.all_for_group(group)
                .order_by("datetime_start")
                .prefetch_related(
                    Prefetch(
                        "participations",
                        to_attr="relevant_participations",
                        queryset=ParticipationStatus.objects.filter(
                            Q(absence_reason__isnull=False) | Q(tardiness__isnull=False)
                        ).select_related("absence_reason", "person"),
                    ),
                    Prefetch(
                        "personal_notes",
                        to_attr="relevant_personal_notes",
                        queryset=PersonalNote.objects.filter(
                            Q(note__gt="") | Q(extra_mark__isnull=False)
                        ).select_related("extra_mark", "person"),
                    ),
                )
            )

    context["groups"] = groups

    recorder.set_progress(3 + len(groups), _number_of_steps, _("Generating template ..."))

    file_object, result = generate_pdf_from_template(
        "alsijil/print/register_for_group.html",
        context,
        file_object=PDFFile.objects.get(pk=file_object),
    )

    recorder.set_progress(4 + len(groups), _number_of_steps, _("Generating PDF ..."))

    with allow_join_result():
        result.wait()
        file_object.refresh_from_db()
        if not (result.status == SUCCESS and file_object.file):
            raise PDFGenerationError(_("PDF generation failed"))

    recorder.set_progress(5 + len(groups), _number_of_steps)


@recorded_task
def generate_person_register_printout(
    person: int,
    school_term: int,
    file_object: int,
    recorder: ProgressRecorder,
):
    """Generate a register printout as PDF for a person."""

    context = {}

    recorder.set_progress(1, 4, _("Loading data ..."))

    person = Person.objects.get(pk=person)
    school_term = SchoolTerm.objects.get(pk=school_term)

    doc_query_set = Documentation.objects.select_related("subject").prefetch_related("teachers")

    statistics = (
        StatisticsBuilder(Person.objects.filter(id=person.id))
        .use_from_school_term(school_term)
        .annotate_statistics()
        .prefetch_relevant_participations(documentation_with_details=doc_query_set)
        .prefetch_relevant_personal_notes(documentation_with_details=doc_query_set)
        .build()
        .first()
    )

    context["person"] = statistics

    context["school_term"] = school_term

    context["absence_reasons"] = AbsenceReason.objects.filter(
        tags__short_name="class_register", count_as_absent=True
    )
    context["absence_reasons_not_counted"] = AbsenceReason.objects.filter(
        tags__short_name="class_register", count_as_absent=False
    )
    context["extra_marks"] = ExtraMark.objects.all()

    recorder.set_progress(2, 4, _("Generating template ..."))

    file_object, result = generate_pdf_from_template(
        "alsijil/print/register_for_person.html",
        context,
        file_object=PDFFile.objects.get(pk=file_object),
    )

    recorder.set_progress(3, 4, _("Generating PDF ..."))

    with allow_join_result():
        result.wait()
        file_object.refresh_from_db()
        if not (result.status == SUCCESS and file_object.file):
            raise PDFGenerationError(_("PDF generation failed"))

    recorder.set_progress(4, 4)
