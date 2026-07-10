from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from projects.models import Project, Workspace
from tasks.models import Task


@login_required
def dashboard_home(request):

    workspaces = Workspace.objects.filter(
        members=request.user,
    )

    projects = Project.objects.filter(
        workspace__in=workspaces,
    )

    tasks = Task.objects.filter(
        project__workspace__in=workspaces,
    )

    todo_count = tasks.filter(status="todo").count()
    in_progress_count = tasks.filter(status="in_progress").count()
    done_count = tasks.filter(status="done").count()

    my_tasks_count = tasks.filter(
        assigned_to=request.user,
    ).count()

    recent_tasks = tasks.order_by("-created_at")[:5]

    context = {
        "workspace_count": workspaces.count(),
        "project_count": projects.count(),
        "task_count": tasks.count(),
        "todo_count": todo_count,
        "in_progress_count": in_progress_count,
        "done_count": done_count,
        "my_tasks_count": my_tasks_count,
        "recent_tasks": recent_tasks,
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context,
    )
