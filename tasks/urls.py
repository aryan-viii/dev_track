from django.urls import path

from . import views

urlpatterns = [

    path(
        "workspaces/<int:workspace_pk>/projects/<int:project_pk>/tasks/",
        views.task_list,
        name="task_list",
    ),

    path(
        "workspaces/<int:workspace_pk>/projects/<int:project_pk>/tasks/create/",
        views.task_create,
        name="task_create",
    ),

    path(
        "workspaces/<int:workspace_pk>/projects/<int:project_pk>/tasks/<int:pk>/",
        views.task_detail,
        name="task_detail",
    ),

    path(
        "workspaces/<int:workspace_pk>/projects/<int:project_pk>/tasks/<int:pk>/edit/",
        views.task_update,
        name="task_update",
    ),

    path(
        "workspaces/<int:workspace_pk>/projects/<int:project_pk>/tasks/<int:pk>/delete/",
        views.task_delete,
        name="task_delete",
    ),

]
