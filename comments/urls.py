from django.urls import path

from . import views

urlpatterns = [

    path(
        "workspaces/<int:workspace_pk>/projects/<int:project_pk>/tasks/<int:task_pk>/comments/create/",
        views.comment_create,
        name="comment_create",
    ),

    path(
        "workspaces/<int:workspace_pk>/projects/<int:project_pk>/tasks/<int:task_pk>/comments/<int:pk>/edit/",
        views.comment_update,
        name="comment_update",
    ),

    path(
        "workspaces/<int:workspace_pk>/projects/<int:project_pk>/tasks/<int:task_pk>/comments/<int:pk>/delete/",
        views.comment_delete,
        name="comment_delete",
    ),

]
