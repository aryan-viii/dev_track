from django import forms

from .models import Workspace


class WorkspaceForm(forms.ModelForm):

    class Meta:
        model = Workspace

        fields = [
            "name",
            "description",
            "logo",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter workspace name",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Describe your workspace...",
                }
            ),

            "logo": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }

        labels = {
            "name": "Workspace Name",
            "description": "Description",
            "logo": "Workspace Logo",
        }

        help_texts = {
            "logo": "Upload a logo (optional).",
        }