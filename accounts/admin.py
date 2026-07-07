from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Profile Information",
            {
                "fields": (
                    "profile_picture",
                    "bio",
                    "github_url",
                    "linkedin_url",
                ),
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Profile Information",
            {
                "fields": (
                    "profile_picture",
                    "bio",
                    "github_url",
                    "linkedin_url",
                ),
            },
        ),
    )