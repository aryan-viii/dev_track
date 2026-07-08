from django.contrib import admin

from .models import Workspace


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

    list_filter = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    filter_horizontal = (
        "members",
    )