from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from projects.models import Project

from comments.forms import CommentForm

from .forms import TaskForm
from .models import Task


def _get_project_or_403(request, workspace_pk, project_pk):
    """
    Helper that fetches a project scoped to its workspace and
    verifies the current user is a member of that workspace.
    Returns (project, None) on success or (None, response) on failure.
    """
    project = get_object_or_404(
        Project,
        pk=project_pk,
        workspace__pk=workspace_pk,
    )

    if request.user not in project.workspace.members.all():
        return None, HttpResponseForbidden(
            "You don't have permission to view this project."
        )

    return project, None


@login_required
def task_list(request, workspace_pk, project_pk):

    project, forbidden = _get_project_or_403(
        request,
        workspace_pk,
        project_pk,
    )

    if forbidden:
        return forbidden

    tasks = project.tasks.all()

    status_filter = request.GET.get("status", "")
    priority_filter = request.GET.get("priority", "")
    search_query = request.GET.get("q", "")

    if status_filter:
        tasks = tasks.filter(status=status_filter)

    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)

    if search_query:
        tasks = tasks.filter(title__icontains=search_query)

    paginator = Paginator(tasks, 8)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {
        "project": project,
        "workspace": project.workspace,
        "tasks": page_obj,
        "page_obj": page_obj,
        "status_filter": status_filter,
        "priority_filter": priority_filter,
        "search_query": search_query,
        "status_choices": Task.STATUS_CHOICES,
        "priority_choices": Task.PRIORITY_CHOICES,
    }

    return render(
        request,
        "tasks/task_list.html",
        context,
    )


@login_required
def task_detail(request, workspace_pk, project_pk, pk):

    project, forbidden = _get_project_or_403(
        request,
        workspace_pk,
        project_pk,
    )

    if forbidden:
        return forbidden

    task = get_object_or_404(
        Task,
        pk=pk,
        project=project,
    )

    context = {
        "project": project,
        "workspace": project.workspace,
        "task": task,
        "comment_form": CommentForm(),
    }

    return render(
        request,
        "tasks/task_detail.html",
        context,
    )


@login_required
def task_create(request, workspace_pk, project_pk):

    project, forbidden = _get_project_or_403(
        request,
        workspace_pk,
        project_pk,
    )

    if forbidden:
        return forbidden

    if request.method == "POST":

        form = TaskForm(
            request.POST,
            workspace=project.workspace,
        )

        if form.is_valid():

            task = form.save(commit=False)

            task.project = project

            task.save()

            messages.success(
                request,
                "Task created successfully!",
            )

            return redirect(
                "task_detail",
                workspace_pk=project.workspace.pk,
                project_pk=project.pk,
                pk=task.pk,
            )

    else:

        form = TaskForm(
            workspace=project.workspace,
        )

    context = {
        "form": form,
        "project": project,
        "workspace": project.workspace,
    }

    return render(
        request,
        "tasks/task_form.html",
        context,
    )


@login_required
def task_update(request, workspace_pk, project_pk, pk):

    project, forbidden = _get_project_or_403(
        request,
        workspace_pk,
        project_pk,
    )

    if forbidden:
        return forbidden

    task = get_object_or_404(
        Task,
        pk=pk,
        project=project,
    )

    if request.method == "POST":

        form = TaskForm(
            request.POST,
            instance=task,
            workspace=project.workspace,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Task updated successfully!",
            )

            return redirect(
                "task_detail",
                workspace_pk=project.workspace.pk,
                project_pk=project.pk,
                pk=task.pk,
            )

    else:

        form = TaskForm(
            instance=task,
            workspace=project.workspace,
        )

    context = {
        "form": form,
        "project": project,
        "workspace": project.workspace,
        "task": task,
    }

    return render(
        request,
        "tasks/task_form.html",
        context,
    )


@login_required
def task_delete(request, workspace_pk, project_pk, pk):

    project, forbidden = _get_project_or_403(
        request,
        workspace_pk,
        project_pk,
    )

    if forbidden:
        return forbidden

    task = get_object_or_404(
        Task,
        pk=pk,
        project=project,
    )

    if request.method == "POST":

        task.delete()

        messages.success(
            request,
            "Task deleted successfully!",
        )

        return redirect(
            "task_list",
            workspace_pk=project.workspace.pk,
            project_pk=project.pk,
        )

    context = {
        "project": project,
        "workspace": project.workspace,
        "task": task,
    }

    return render(
        request,
        "tasks/task_confirm_delete.html",
        context,
    )
