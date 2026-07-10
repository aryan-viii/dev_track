from django import forms

from .models import Task


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task

        fields = [
            "title",
            "description",
            "assigned_to",
            "status",
            "priority",
            "due_date",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter task title",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Describe the task...",
                }
            ),

            "assigned_to": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "priority": forms.Select(
                attrs={
                    "class": "form-select",
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
            "title": "Task Title",
            "description": "Description",
            "assigned_to": "Assign To",
            "status": "Status",
            "priority": "Priority",
            "due_date": "Due Date",
        }

    def __init__(self, *args, workspace=None, **kwargs):
        super().__init__(*args, **kwargs)

        if workspace is not None:
            self.fields["assigned_to"].queryset = workspace.members.all()

        self.fields["assigned_to"].required = False
