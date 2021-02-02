from django.contrib import admin
from django.db.models import Avg, Max, Min
from django.http import HttpRequest

from .models import Category, Issue


class CategoryAdmin(admin.ModelAdmin):
    """Categories are only visible to superusers"""


class IssueAdmin(admin.ModelAdmin):
    """Issue Admin - visible and editable by staff"""

    # fields =
    list_display = ["pk", "category", "title", "status", "reporter", "assignee"]
    list_display_links = ["pk", "title"]

    def has_view_permission(self, request, obj=None) -> bool:
        return request.user.is_staff or request.user.is_superuser

    def has_module_permission(self, request) -> bool:
        return request.user.is_staff or request.user.is_superuser

    def get_form(self, request: HttpRequest, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if request.user.is_superuser:
            # pre-fill reporter with current user value
            form.base_fields["reporter"].initial = request.user
        return form

    def changelist_view(self, request, extra_context=None):
        aggregates = Issue.objects.aggregate(
            Avg("spent_time"), Max("spent_time"), Min("spent_time")
        )
        context = {
            "spent_time_average": aggregates["spent_time__avg"],
            "spent_time_max": aggregates["spent_time__max"],
            "spent_time_min": aggregates["spent_time__min"],
        }
        if extra_context:
            context.update(extra_context)
        return super().changelist_view(request, context)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Issue, IssueAdmin)
