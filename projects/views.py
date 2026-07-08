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