from django.db.models import FilteredRelation, Prefetch, Q, QuerySet, Value
from django.db.models.aggregates import Count, Sum

from aleksis.apps.chronos.models import LessonEvent
from aleksis.apps.kolego.models import AbsenceReason
from aleksis.core.models import Group, Person, SchoolTerm

from ..models import Documentation, ExtraMark, ParticipationStatus, PersonalNote


class BuilderError(Exception):
    """Error in building statistics using the StatisticsBuilder."""

    pass


class StatisticsBuilder:
    """Builder class for building queries with annotated statistics on persons.

    To build queries, you can combine `use_` with multiple `annotate` or `prefetch`
    methods. At the end, call `build` to get the actual queryset.

    >>> StatisticsBuilder(person_qs).use_from_school_term(school_term).annotate_statistics().build()
    """

    def __init__(self, persons: QuerySet[Person]) -> None:
        """Intialize the builder with a persons queryset."""
        self.qs: QuerySet[Person] = persons
        self.participations_filter: Q | None = None
        self.personal_notes_filter: Q | None = None
        self.empty: bool = False
        self._order()

    def _order(self) -> "StatisticsBuilder":
        """Order by last and first names."""
        self.qs = self.qs.order_by("last_name", "first_name")
        return self

    def use_participations(
        self,
        participations_filter: Q,
    ) -> "StatisticsBuilder":
        """Set a filter for participations."""
        self.participations_filter = participations_filter
        return self

    def use_personal_notes(
        self,
        personal_notes_filter: Q,
    ) -> "StatisticsBuilder":
        """Set a filter for personal notes."""
        self.personal_notes_filter = personal_notes_filter
        return self

    def use_from_documentations(
        self, documentations: QuerySet[Documentation]
    ) -> "StatisticsBuilder":
        """Set a filter for participations and personal notes from documentations."""
        docs = list(documentations.values_list("pk", flat=True))
        if len(docs) == 0:
            self.empty = True
        self.use_participations(Q(participations__related_documentation__in=docs))
        self.use_personal_notes(Q(personal_notes__documentation__in=docs))
        return self

    def use_from_school_term(self, school_term: SchoolTerm) -> "StatisticsBuilder":
        """Set a filter for participations and personal notes from school term."""
        documentations = Documentation.objects.for_school_term(school_term)
        self.use_from_documentations(documentations)
        return self

    def use_from_group(
        self, group: Group, school_term: SchoolTerm | None = None
    ) -> "StatisticsBuilder":
        """Set a filter for participations and personal notes from group."""
        school_term = school_term or group.school_term
        if not school_term:
            documentations = Documentation.objects.none()
        else:
            lesson_events = LessonEvent.objects.filter(LessonEvent.objects.for_group_q(group))
            documentations = Documentation.objects.for_school_term(school_term).filter(
                amends__in=lesson_events
            )
        self.use_from_documentations(documentations)
        return self

    def _annotate_filtered_participations(self, condition: Q | None = None) -> "StatisticsBuilder":
        """Annotate a filtered relation for participations."""
        if not self.participations_filter and not condition:
            raise BuilderError("Annotation of participations needs a participation filter.")
        self.qs = self.qs.annotate(
            filtered_participation_statuses=FilteredRelation(
                "participations",
                condition=condition or self.participations_filter,
            )
        )
        return self

    def _annotate_filtered_personal_notes(self, condition: Q | None = None) -> "StatisticsBuilder":
        """Annotate a filtered relation for personal notes."""
        if not self.personal_notes_filter and not condition:
            raise BuilderError("Annotation of personal notes needs a participation filter.")
        self.qs = self.qs.annotate(
            filtered_personal_notes=FilteredRelation(
                "personal_notes",
                condition=condition or self.personal_notes_filter,
            ),
        )
        return self

    def annotate_participation_statistics(self) -> "StatisticsBuilder":
        """Annotate statistics for participations."""
        if self.empty:
            self.annotate_empty_participation_statistics()
            return self
        self._annotate_filtered_participations()

        self.qs = self.qs.annotate(
            participation_count=Count(
                "filtered_participation_statuses",
                filter=Q(filtered_participation_statuses__absence_reason__isnull=True),
                distinct=True,
            ),
            absence_count=Count(
                "filtered_participation_statuses",
                filter=Q(filtered_participation_statuses__absence_reason__count_as_absent=True),
                distinct=True,
            ),
            tardiness_sum=Sum("filtered_participation_statuses__tardiness", distinct=True),
            tardiness_count=Count(
                "filtered_participation_statuses",
                filter=Q(filtered_participation_statuses__tardiness__gt=0),
                distinct=True,
            ),
        )

        for absence_reason in AbsenceReason.objects.all():
            self.qs = self.qs.annotate(
                **{
                    absence_reason.count_label: Count(
                        "filtered_participation_statuses",
                        filter=Q(
                            filtered_participation_statuses__absence_reason=absence_reason,
                        ),
                        distinct=True,
                    )
                }
            )

        return self

    def annotate_personal_note_statistics(self) -> "StatisticsBuilder":
        """Annotate statistics for personal notes."""
        if self.empty:
            self.annotate_empty_personal_note_statistics()
            return self
        self._annotate_filtered_personal_notes()

        for extra_mark in ExtraMark.objects.all():
            self.qs = self.qs.annotate(
                **{
                    extra_mark.count_label: Count(
                        "filtered_personal_notes",
                        filter=Q(filtered_personal_notes__extra_mark=extra_mark),
                        distinct=True,
                    )
                }
            )

        return self

    def annotate_statistics(self) -> "StatisticsBuilder":
        """Annotate statistics for participations and personal notes."""
        self.annotate_participation_statistics()
        self.annotate_personal_note_statistics()

        return self

    def annotate_empty_participation_statistics(self) -> "StatisticsBuilder":
        """Annotate with empty participation statistics."""
        self.qs = self.qs.annotate(
            absence_count=Value(0),
            participation_count=Value(0),
            tardiness_count=Value(0),
            tardiness_sum=Value(0),
        )
        for absence_reason in AbsenceReason.objects.all():
            self.qs = self.qs.annotate(**{absence_reason.count_label: Value(0)})

        return self

    def annotate_empty_personal_note_statistics(self) -> "StatisticsBuilder":
        """Annotate with empty personal note statistics."""
        for extra_mark in ExtraMark.objects.all():
            self.qs = self.qs.annotate(**{extra_mark.count_label: Value(0)})

        return self

    def annotate_empty_statistics(self) -> "StatisticsBuilder":
        """Annotate with empty statistics."""
        self.annotate_empty_participation_statistics()
        self.annotate_empty_personal_note_statistics()

        return self

    def prefetch_relevant_participations(
        self,
        select_related: list | None = None,
        prefetch_related: list | None = None,
        documentation_with_details: QuerySet | None = None,
    ) -> "StatisticsBuilder":
        """Prefetch relevant participations."""
        if not select_related:
            select_related = []
        if not prefetch_related:
            prefetch_related = []

        if documentation_with_details:
            prefetch_related.append(
                Prefetch("related_documentation", queryset=documentation_with_details)
            )
        else:
            select_related.append("related_documentation")
        self.qs = self.qs.prefetch_related(
            Prefetch(
                "participations",
                to_attr="relevant_participations",
                queryset=ParticipationStatus.objects.filter(
                    Q(absence_reason__isnull=False) | Q(tardiness__isnull=False)
                )
                .select_related("absence_reason", *select_related)
                .prefetch_related(*prefetch_related),
            )
        )

        return self

    def prefetch_relevant_personal_notes(
        self,
        select_related: list | None = None,
        prefetch_related: list | None = None,
        documentation_with_details: QuerySet | None = None,
    ) -> "StatisticsBuilder":
        """Prefetch relevant personal notes."""
        if not select_related:
            select_related = []
        if not prefetch_related:
            prefetch_related = []

        if documentation_with_details:
            prefetch_related.append(Prefetch("documentation", queryset=documentation_with_details))
        else:
            select_related.append("documentation")

        self.qs = self.qs.prefetch_related(
            Prefetch(
                "personal_notes",
                to_attr="relevant_personal_notes",
                queryset=PersonalNote.objects.filter(Q(note__gt="") | Q(extra_mark__isnull=False))
                .select_related("extra_mark", *select_related)
                .prefetch_related(*prefetch_related),
            )
        )

        return self

    def build(self) -> QuerySet[Person]:
        """Build annotated queryset with statistics."""
        return self.qs
