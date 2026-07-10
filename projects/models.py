from django.conf import settings
from django.db import models


class Workspace(models.Model):
    name = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True
    )

    logo = models.ImageField(
        upload_to="workspace_logos/",
        blank=True,
        null=True
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_workspaces"
    )

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="workspaces",
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
    

class Project(models.Model):

    STATUS_CHOICES = [
        ("planning", "Planning"),
        ("active", "Active"),
        ("completed", "Completed"),
        ("archived", "Archived"),
    ]

    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="projects",
    )

    name = models.CharField(
        max_length=150,
    )

    description = models.TextField(
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="planning",
    )

    start_date = models.DateField(
        null=True,
        blank=True,
    )

    due_date = models.DateField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name