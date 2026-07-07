from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True,
    )

    bio = models.TextField(
        max_length=500,
        blank=True,
    )

    github_url = models.URLField(
        blank=True,
    )

    linkedin_url = models.URLField(
        blank=True,
    )

    def __str__(self):
        return self.username