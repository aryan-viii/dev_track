from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from projects.models import Project, Workspace

from .models import Task

User = get_user_model()


class TaskModelTests(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner",
            password="testpass123",
        )

        self.assignee = User.objects.create_user(
            username="assignee",
            password="testpass123",
        )

        self.workspace = Workspace.objects.create(
            name="Test Workspace",
            owner=self.owner,
        )
        self.workspace.members.add(self.owner, self.assignee)

        self.project = Project.objects.create(
            workspace=self.workspace,
            name="Test Project",
        )

        self.task = Task.objects.create(
            project=self.project,
            title="Test Task",
            assigned_to=self.assignee,
            status="todo",
            priority="high",
        )

    def test_task_str(self):
        self.assertEqual(str(self.task), "Test Task")

    def test_task_belongs_to_project(self):
        self.assertEqual(self.task.project, self.project)

    def test_task_appears_in_project_related_name(self):
        self.assertIn(self.task, self.project.tasks.all())

    def test_unassigning_user_does_not_delete_task(self):
        # assigned_to uses SET_NULL, so deleting the assignee (who is
        # not the workspace owner) should not cascade-delete the task —
        # it should just null out the assignment.
        self.assignee.delete()

        self.task.refresh_from_db()

        self.assertIsNone(self.task.assigned_to)
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())


class TaskViewTests(TestCase):

    def setUp(self):
        self.member = User.objects.create_user(
            username="member",
            password="testpass123",
        )

        self.workspace = Workspace.objects.create(
            name="Test Workspace",
            owner=self.member,
        )
        self.workspace.members.add(self.member)

        self.project = Project.objects.create(
            workspace=self.workspace,
            name="Test Project",
        )

        self.client.login(username="member", password="testpass123")

    def test_task_create(self):
        response = self.client.post(
            reverse(
                "task_create",
                args=[self.workspace.pk, self.project.pk],
            ),
            {
                "title": "New Task",
                "description": "",
                "status": "todo",
                "priority": "medium",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Task.objects.filter(title="New Task").exists()
        )

    def test_task_list_search_filters_by_title(self):
        Task.objects.create(project=self.project, title="Fix login bug")
        Task.objects.create(project=self.project, title="Write docs")

        response = self.client.get(
            reverse(
                "task_list",
                args=[self.workspace.pk, self.project.pk],
            ),
            {"q": "login"},
        )

        self.assertContains(response, "Fix login bug")
        self.assertNotContains(response, "Write docs")

    def test_task_list_status_filter(self):
        Task.objects.create(
            project=self.project,
            title="Todo Task",
            status="todo",
        )
        Task.objects.create(
            project=self.project,
            title="Done Task",
            status="done",
        )

        response = self.client.get(
            reverse(
                "task_list",
                args=[self.workspace.pk, self.project.pk],
            ),
            {"status": "done"},
        )

        self.assertContains(response, "Done Task")
        self.assertNotContains(response, "Todo Task")