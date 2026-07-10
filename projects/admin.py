from django.contrib import admin

from .models import Workspace, Project


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
        "created_at",
    )

    search_fields = (
        "name",
        "owner__username",
    )

    filter_horizontal = (
        "members",
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "workspace",
        "status",
        "due_date",
    )

    list_filter = (
        "status",
        "workspace",
    )

    search_fields = (
        "name",
        "workspace__name",
    )

    ordering = (
        "-created_at",
    )