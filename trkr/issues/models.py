from datetime import timedelta

from django.conf import settings
from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=50)
    is_archived = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title


class Issue(models.Model):
    STATUS_BACKLOG = "B"
    STATUS_TO_DO_NOW = "T"
    STATUS_IN_PROGRESS = "I"
    STATUS_WAITING_FOR_REVIEW = "W"
    STATUS_RESOLVED = "R"
    STATUS_CLOSED = "C"
    STATUS_CHOICES = (
        (STATUS_BACKLOG, "In Backlog"),
        (STATUS_TO_DO_NOW, "To Do Now"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_WAITING_FOR_REVIEW, "Waiting For Review"),
        (STATUS_RESOLVED, "Resolved"),
        (STATUS_CLOSED, "Closed"),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        limit_choices_to={"is_archived": False},
        blank=False,
        null=False,
    )
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        limit_choices_to={"is_active": True},
        related_name="reported_issues",
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        limit_choices_to={"is_active": True},
        related_name="assigned_issues",
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=STATUS_BACKLOG,
    )
    estimated_time = models.DurationField(
        default=timedelta(),
        null=False,
    )
    spent_time = models.DurationField(
        default=timedelta(),
        null=False,
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"#{self.pk} - {self.title} ({self.get_status_display()})"
