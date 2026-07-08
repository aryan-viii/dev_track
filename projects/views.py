from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseForbidden

from .forms import WorkspaceForm
from .models import Workspace


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