from django.urls import path

from . import views

urlpatterns = [
    path(
        "workspaces/",
        views.workspace_list,
        name="workspace_list",
    ),

    path(
        "workspaces/create/",
        views.workspace_create,
        name="workspace_create",
    ),

    path(
        "workspaces/<int:pk>/",
        views.workspace_detail,
        name="workspace_detail",
    ),

    path(
        "workspaces/<int:pk>/edit/",
        views.workspace_update,
        name="workspace_update",
    ),

    path(
        "workspaces/<int:pk>/delete/",
        views.workspace_delete,
        name="workspace_delete",
    ),

    path(
        "workspaces/<int:workspace_pk>/projects/",
        views.project_list,
        name="project_list",
    ),

    path(
        "workspaces/<int:workspace_pk>/projects/create/",
        views.project_create,
        name="project_create",
    ),

    path(
        "workspaces/<int:workspace_pk>/projects/<int:pk>/",
        views.project_detail,
        name="project_detail",
    ),

    path(
        "workspaces/<int:workspace_pk>/projects/<int:pk>/edit/",
        views.project_update,
        name="project_update",
    ),

    path(
        "workspaces/<int:workspace_pk>/projects/<int:pk>/delete/",
        views.project_delete,
        name="project_delete",
    ),
]