from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from tasks.models import Task

from .forms import CommentForm
from .models import Comment


def _get_task_or_403(request, workspace_pk, project_pk, task_pk):
    """
    Helper that fetches a task scoped to its project/workspace and
    verifies the current user is a member of that workspace.
    Returns (task, None) on success or (None, response) on failure.
    """
    task = get_object_or_404(
        Task,
        pk=task_pk,
        project__pk=project_pk,
        project__workspace__pk=workspace_pk,
    )

    if request.user not in task.project.workspace.members.all():
        return None, HttpResponseForbidden(
            "You don't have permission to view this task."
        )

    return task, None


@login_required
def comment_create(request, workspace_pk, project_pk, task_pk):

    task, forbidden = _get_task_or_403(
        request,
        workspace_pk,
        project_pk,
        task_pk,
    )

    if forbidden:
        return forbidden

    if request.method == "POST":

        form = CommentForm(request.POST)

        if form.is_valid():

            comment = form.save(commit=False)

            comment.task = task
            comment.author = request.user

            comment.save()

            messages.success(
                request,
                "Comment added successfully!",
            )

    return redirect(
        "task_detail",
        workspace_pk=task.project.workspace.pk,
        project_pk=task.project.pk,
        pk=task.pk,
    )


@login_required
def comment_update(request, workspace_pk, project_pk, task_pk, pk):

    task, forbidden = _get_task_or_403(
        request,
        workspace_pk,
        project_pk,
        task_pk,
    )

    if forbidden:
        return forbidden

    comment = get_object_or_404(
        Comment,
        pk=pk,
        task=task,
    )

    if comment.author != request.user:

        messages.error(
            request,
            "You don't have permission to edit this comment.",
        )

        return redirect(
            "task_detail",
            workspace_pk=task.project.workspace.pk,
            project_pk=task.project.pk,
            pk=task.pk,
        )

    if request.method == "POST":

        form = CommentForm(
            request.POST,
            instance=comment,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Comment updated successfully!",
            )

            return redirect(
                "task_detail",
                workspace_pk=task.project.workspace.pk,
                project_pk=task.project.pk,
                pk=task.pk,
            )

    else:

        form = CommentForm(
            instance=comment,
        )

    context = {
        "form": form,
        "task": task,
        "project": task.project,
        "workspace": task.project.workspace,
        "comment": comment,
    }

    return render(
        request,
        "comments/comment_form.html",
        context,
    )


@login_required
def comment_delete(request, workspace_pk, project_pk, task_pk, pk):

    task, forbidden = _get_task_or_403(
        request,
        workspace_pk,
        project_pk,
        task_pk,
    )

    if forbidden:
        return forbidden

    comment = get_object_or_404(
        Comment,
        pk=pk,
        task=task,
    )

    if comment.author != request.user:

        messages.error(
            request,
            "You don't have permission to delete this comment.",
        )

        return redirect(
            "task_detail",
            workspace_pk=task.project.workspace.pk,
            project_pk=task.project.pk,
            pk=task.pk,
        )

    if request.method == "POST":

        comment.delete()

        messages.success(
            request,
            "Comment deleted successfully!",
        )

        return redirect(
            "task_detail",
            workspace_pk=task.project.workspace.pk,
            project_pk=task.project.pk,
            pk=task.pk,
        )

    context = {
        "task": task,
        "project": task.project,
        "workspace": task.project.workspace,
        "comment": comment,
    }

    return render(
        request,
        "comments/comment_confirm_delete.html",
        context,
    )
