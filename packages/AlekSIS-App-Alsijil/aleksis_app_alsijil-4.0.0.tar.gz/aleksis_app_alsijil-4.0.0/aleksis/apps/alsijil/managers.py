from collections.abc import Sequence
from datetime import date, datetime
from typing import TYPE_CHECKING, Optional, Union

from django.db.models import QuerySet
from django.db.models.query import Prefetch
from django.db.models.query_utils import Q

from calendarweek import CalendarWeek

from aleksis.apps.chronos.models import LessonEvent
from aleksis.core.managers import (
    AlekSISBaseManagerWithoutMigrations,
    CalendarEventManager,
)

if TYPE_CHECKING:
    from aleksis.core.models import Group, SchoolTerm

    from .models import Documentation


class GroupRoleManager(AlekSISBaseManagerWithoutMigrations):
    pass


class GroupRoleQuerySet(QuerySet):
    def with_assignments(
        self, time_ref: Union[date, CalendarWeek], groups: Sequence["Group"]
    ) -> QuerySet:
        from aleksis.apps.alsijil.models import GroupRoleAssignment

        if isinstance(time_ref, CalendarWeek):
            qs = GroupRoleAssignment.objects.in_week(time_ref)
        else:
            qs = GroupRoleAssignment.objects.on_day(time_ref)

        qs = qs.for_groups(groups).distinct()
        return self.prefetch_related(
            Prefetch(
                "assignments",
                queryset=qs,
            )
        )


class GroupRoleAssignmentManager(AlekSISBaseManagerWithoutMigrations):
    pass


class GroupRoleAssignmentQuerySet(QuerySet):
    def within_dates(self, start: date, end: date):
        """Filter for all role assignments within a date range."""
        return self.filter(
            Q(date_start__lte=end) & (Q(date_end__gte=start) | Q(date_end__isnull=True))
        )

    def at_time(self, when: Optional[datetime] = None):
        """Filter for role assignments assigned at a certain point in time."""
        now = when or datetime.now()

        return self.on_day(now.date())

    def for_groups(self, groups: Sequence["Group"]):
        """Filter all role assignments for a sequence of groups."""
        qs = self
        for group in groups:
            qs = qs.for_group(group)
        return qs

    def for_group(self, group: "Group"):
        """Filter all role assignments for a group."""
        return self.filter(Q(groups=group) | Q(groups__child_groups=group))


class DocumentationManager(CalendarEventManager):
    """Manager adding specific methods to documentations."""

    def for_school_term(self, school_term: "SchoolTerm") -> QuerySet["Documentation"]:
        """Filter documentations by school term."""
        return self.filter(
            datetime_start__date__gte=school_term.date_start,
            datetime_end__date__lte=school_term.date_end,
        )

    def all_for_group(self, group: "Group") -> QuerySet["Documentation"]:
        """Filter documentations by group."""
        qs = self.for_school_term(group.school_term) if group.school_term else self
        return qs.filter(
            pk__in=self.filter(course__groups=group)
            .values_list("pk", flat=True)
            .union(self.filter(course__groups__parent_groups=group).values_list("pk", flat=True))
            .union(
                self.filter(
                    amends__in=LessonEvent.objects.filter(LessonEvent.objects.for_group_q(group))
                ).values_list("pk", flat=True)
            )
        )

    def all_planned_for_group(self, group: "Group") -> QuerySet["Documentation"]:
        """Filter documentations by group, but only planned lessons."""
        qs = self.for_school_term(group.school_term) if group.school_term else self
        return qs.filter(
            pk__in=self.filter(
                amends__in=LessonEvent.objects.filter(LessonEvent.objects.for_group_q(group))
            ).values_list("pk", flat=True)
        )


class ParticipationStatusManager(CalendarEventManager):
    """Manager adding specific methods to participation statuses."""

    pass
