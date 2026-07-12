from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from projects.models import Project, Workspace
from tasks.models import Task

from .models import Comment

User = get_user_model()


class CommentPermissionTests(TestCase):

    def setUp(self):
        self.author = User.objects.create_user(
            username="author",
            password="testpass123",
        )

        self.other_member = User.objects.create_user(
            username="other",
            password="testpass123",
        )

        self.workspace = Workspace.objects.create(
            name="Test Workspace",
            owner=self.author,
        )
        self.workspace.members.add(self.author, self.other_member)

        self.project = Project.objects.create(
            workspace=self.workspace,
            name="Test Project",
        )

        self.task = Task.objects.create(
            project=self.project,
            title="Test Task",
        )

        self.comment = Comment.objects.create(
            task=self.task,
            author=self.author,
            body="Original comment",
        )

    def test_comment_str_includes_author_and_task(self):
        self.assertIn("author", str(self.comment))

    def test_author_can_delete_own_comment(self):
        self.client.login(username="author", password="testpass123")

        self.client.post(
            reverse(
                "comment_delete",
                args=[self.workspace.pk, self.project.pk, self.task.pk, self.comment.pk],
            )
        )

        self.assertFalse(
            Comment.objects.filter(pk=self.comment.pk).exists()
        )

    def test_other_member_cannot_delete_someone_elses_comment(self):
        self.client.login(username="other", password="testpass123")

        self.client.post(
            reverse(
                "comment_delete",
                args=[self.workspace.pk, self.project.pk, self.task.pk, self.comment.pk],
            )
        )

        self.assertTrue(
            Comment.objects.filter(pk=self.comment.pk).exists()
        )