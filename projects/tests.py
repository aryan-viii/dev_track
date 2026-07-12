from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Project, Workspace

User = get_user_model()


class WorkspaceModelTests(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner",
            password="testpass123",
        )

        self.workspace = Workspace.objects.create(
            name="Test Workspace",
            owner=self.owner,
        )
        self.workspace.members.add(self.owner)

    def test_workspace_str(self):
        self.assertEqual(str(self.workspace), "Test Workspace")

    def test_owner_is_member(self):
        self.assertIn(self.owner, self.workspace.members.all())


class ProjectModelTests(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner",
            password="testpass123",
        )

        self.workspace = Workspace.objects.create(
            name="Test Workspace",
            owner=self.owner,
        )

        self.project = Project.objects.create(
            workspace=self.workspace,
            name="Test Project",
            status="active",
        )

    def test_project_str(self):
        self.assertEqual(str(self.project), "Test Project")

    def test_project_belongs_to_workspace(self):
        self.assertEqual(self.project.workspace, self.workspace)

    def test_project_appears_in_workspace_related_name(self):
        self.assertIn(self.project, self.workspace.projects.all())


class WorkspacePermissionTests(TestCase):
    """
    Non-members should never be able to view or edit a workspace
    or its projects.
    """

    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner",
            password="testpass123",
        )

        self.outsider = User.objects.create_user(
            username="outsider",
            password="testpass123",
        )

        self.workspace = Workspace.objects.create(
            name="Private Workspace",
            owner=self.owner,
        )
        self.workspace.members.add(self.owner)

    def test_member_can_view_workspace(self):
        self.client.login(username="owner", password="testpass123")

        response = self.client.get(
            reverse("workspace_detail", args=[self.workspace.pk])
        )

        self.assertEqual(response.status_code, 200)

    def test_non_member_cannot_view_workspace(self):
        self.client.login(username="outsider", password="testpass123")

        response = self.client.get(
            reverse("workspace_detail", args=[self.workspace.pk])
        )

        self.assertEqual(response.status_code, 403)

    def test_anonymous_user_redirected_to_login(self):
        response = self.client.get(
            reverse("workspace_detail", args=[self.workspace.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_non_owner_cannot_delete_project(self):
        project = Project.objects.create(
            workspace=self.workspace,
            name="Owner's Project",
        )

        self.workspace.members.add(self.outsider)

        self.client.login(username="outsider", password="testpass123")

        response = self.client.post(
            reverse(
                "project_delete",
                args=[self.workspace.pk, project.pk],
            )
        )

        # Redirected away, not deleted
        self.assertTrue(Project.objects.filter(pk=project.pk).exists())
        self.assertEqual(response.status_code, 302)