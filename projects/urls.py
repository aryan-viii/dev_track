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
]