from django import forms

from .models import Workspace, Project


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


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project

        fields = [
            "name",
            "description",
            "status",
            "start_date",
            "due_date",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter project name",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Describe your project...",
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "start_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "due_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
        }

        labels = {
            "name": "Project Name",
            "description": "Description",
            "status": "Status",
            "start_date": "Start Date",
            "due_date": "Due Date",
        }