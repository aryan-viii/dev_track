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
]