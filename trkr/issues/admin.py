from django.contrib import admin
from django.http import HttpRequest

from .models import Category, Issue


class CategoryAdmin(admin.ModelAdmin):
    """Categories are only visible to superusers"""


class IssueAdmin(admin.ModelAdmin):
    """Issue Admin - visible and editable by staff
    TODO archived issue is not editable
    TODO maybe create "issue admin" user group so some users can edit and create issues without
    """

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


admin.site.register(Category, CategoryAdmin)
admin.site.register(Issue, IssueAdmin)
