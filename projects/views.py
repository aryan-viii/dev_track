from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden

from .forms import WorkspaceForm, ProjectForm
from .models import Workspace, Project


@login_required
def workspace_list(request):

    workspaces = Workspace.objects.filter(
        members=request.user
    ).order_by("-created_at")

    context = {
        "workspaces": workspaces,
    }

    return render(
        request,
        "projects/workspace_list.html",
        context,
    )


@login_required
def workspace_detail(request, pk):

    workspace = get_object_or_404(
        Workspace,
        pk=pk
    )

    if request.user not in workspace.members.all():
        return HttpResponseForbidden(
            "You don't have permission to view this workspace."
        )

    context = {
        "workspace": workspace,
    }

    return render(
        request,
        "projects/workspace_detail.html",
        context,
    )


@login_required
def workspace_create(request):

    if request.method == "POST":

        form = WorkspaceForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            workspace = form.save(commit=False)

            workspace.owner = request.user

            workspace.save()

            workspace.members.add(request.user)

            messages.success(
                request,
                "Workspace created successfully!"
            )

            return redirect(
                "workspace_detail",
                pk=workspace.pk,
            )

    else:

        form = WorkspaceForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "projects/workspace_form.html",
        context,
    )


@login_required
def workspace_update(request, pk):

    workspace = get_object_or_404(
        Workspace,
        pk=pk,
    )

    # Only owner can edit
    if workspace.owner != request.user:

        messages.error(
            request,
            "You don't have permission to edit this workspace.",
        )

        return redirect(
            "workspace_detail",
            pk=workspace.pk,
        )

    if request.method == "POST":

        form = WorkspaceForm(
            request.POST,
            request.FILES,
            instance=workspace,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Workspace updated successfully!",
            )

            return redirect(
                "workspace_detail",
                pk=workspace.pk,
            )

    else:

        form = WorkspaceForm(
            instance=workspace,
        )

    context = {
        "form": form,
        "workspace": workspace,
    }

    return render(
        request,
        "projects/workspace_form.html",
        context,
    )


@login_required
def workspace_delete(request, pk):

    workspace = get_object_or_404(
        Workspace,
        pk=pk,
    )

    if workspace.owner != request.user:

        messages.error(
            request,
            "You don't have permission to delete this workspace.",
        )

        return redirect(
            "workspace_detail",
            pk=workspace.pk,
        )

    if request.method == "POST":

        workspace.delete()

        messages.success(
            request,
            "Workspace deleted successfully!",
        )

        return redirect("workspace_list")

    context = {
        "workspace": workspace,
    }

    return render(
        request,
        "projects/workspace_confirm_delete.html",
        context,
    )


@login_required
def project_list(request, workspace_pk):

    workspace = get_object_or_404(
        Workspace,
        pk=workspace_pk,
    )

    if request.user not in workspace.members.all():
        return HttpResponseForbidden(
            "You don't have permission to view this workspace."
        )

    projects = workspace.projects.all()

    search_query = request.GET.get("q", "")

    if search_query:
        projects = projects.filter(name__icontains=search_query)

    paginator = Paginator(projects, 6)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {
        "workspace": workspace,
        "projects": page_obj,
        "page_obj": page_obj,
        "search_query": search_query,
    }

    return render(
        request,
        "projects/project_list.html",
        context,
    )


@login_required
def project_detail(request, workspace_pk, pk):

    workspace = get_object_or_404(
        Workspace,
        pk=workspace_pk,
    )

    if request.user not in workspace.members.all():
        return HttpResponseForbidden(
            "You don't have permission to view this workspace."
        )

    project = get_object_or_404(
        Project,
        pk=pk,
        workspace=workspace,
    )

    context = {
        "workspace": workspace,
        "project": project,
    }

    return render(
        request,
        "projects/project_detail.html",
        context,
    )


@login_required
def project_create(request, workspace_pk):

    workspace = get_object_or_404(
        Workspace,
        pk=workspace_pk,
    )

    if request.user not in workspace.members.all():
        return HttpResponseForbidden(
            "You don't have permission to view this workspace."
        )

    if request.method == "POST":

        form = ProjectForm(request.POST)

        if form.is_valid():

            project = form.save(commit=False)

            project.workspace = workspace

            project.save()

            messages.success(
                request,
                "Project created successfully!",
            )

            return redirect(
                "project_detail",
                workspace_pk=workspace.pk,
                pk=project.pk,
            )

    else:

        form = ProjectForm()

    context = {
        "form": form,
        "workspace": workspace,
    }

    return render(
        request,
        "projects/project_form.html",
        context,
    )


@login_required
def project_update(request, workspace_pk, pk):

    workspace = get_object_or_404(
        Workspace,
        pk=workspace_pk,
    )

    project = get_object_or_404(
        Project,
        pk=pk,
        workspace=workspace,
    )

    # Only the workspace owner can edit projects
    if workspace.owner != request.user:

        messages.error(
            request,
            "You don't have permission to edit this project.",
        )

        return redirect(
            "project_detail",
            workspace_pk=workspace.pk,
            pk=project.pk,
        )

    if request.method == "POST":

        form = ProjectForm(
            request.POST,
            instance=project,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Project updated successfully!",
            )

            return redirect(
                "project_detail",
                workspace_pk=workspace.pk,
                pk=project.pk,
            )

    else:

        form = ProjectForm(
            instance=project,
        )

    context = {
        "form": form,
        "workspace": workspace,
        "project": project,
    }

    return render(
        request,
        "projects/project_form.html",
        context,
    )


@login_required
def project_delete(request, workspace_pk, pk):

    workspace = get_object_or_404(
        Workspace,
        pk=workspace_pk,
    )

    project = get_object_or_404(
        Project,
        pk=pk,
        workspace=workspace,
    )

    if workspace.owner != request.user:

        messages.error(
            request,
            "You don't have permission to delete this project.",
        )

        return redirect(
            "project_detail",
            workspace_pk=workspace.pk,
            pk=project.pk,
        )

    if request.method == "POST":

        project.delete()

        messages.success(
            request,
            "Project deleted successfully!",
        )

        return redirect(
            "project_list",
            workspace_pk=workspace.pk,
        )

    context = {
        "workspace": workspace,
        "project": project,
    }

    return render(
        request,
        "projects/project_confirm_delete.html",
        context,
    )