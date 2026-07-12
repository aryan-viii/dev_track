# DevTrack

A project & task management app built with Django. Users organize work into
Workspaces, which contain Projects, which contain Tasks, which can be
discussed via Comments.

## Tech Stack

- Python / Django
- SQLite
- Bootstrap 5 (no JS frameworks)
- Pillow (image uploads: profile pictures, workspace logos)

No DRF, Celery, Redis, Docker, or WebSockets — this is intentionally an
intermediate-scope project, not an over-engineered one.

## Data Model

```
User
 └── Workspace (owner, members M2M)
      └── Project
           └── Task (assigned_to → User)
                └── Comment (author → User)
```

- **User** — custom user model (`accounts.User`, extends `AbstractUser`) with
  profile picture and bio.
- **Workspace** — has one `owner` and many `members` (M2M, includes the
  owner). Only members can view a workspace's contents.
- **Project** — belongs to a Workspace. Has a status
  (planning/active/completed/archived), start date, due date.
- **Task** — belongs to a Project. Has a status (todo/in_progress/done), a
  priority (low/medium/high), an optional due date, and an optional
  `assigned_to` (restricted to that workspace's members in the form).
- **Comment** — belongs to a Task, has an `author`. Simple threaded
  discussion on each task.

## Permissions Model

Kept deliberately simple (no roles/groups):

- **View** — any workspace member can view its projects, tasks, and comments.
- **Edit/delete Workspace or Project** — workspace owner only.
- **Create/edit/delete Task** — any workspace member (collaborative by
  design).
- **Edit/delete Comment** — only the comment's own author.

Each view enforces this with an explicit membership/ownership check plus
`get_object_or_404` scoped by parent (e.g. a Task lookup is always filtered
by `project__workspace__pk=workspace_pk`), so you can't reach another
workspace's data by guessing a URL.

## App Layout

| App | Responsibility |
|---|---|
| `accounts` | Custom User model, register/login/logout, profile edit |
| `projects` | Workspace CRUD, Project CRUD |
| `tasks` | Task CRUD, list filtering (status/priority), search, pagination |
| `comments` | Comment CRUD, rendered inline on the task detail page |
| `dashboard` | Aggregate stats + recent tasks across all of a user's workspaces |
| `core` | Static pages (home/about/contact) |

URLs are nested to reflect the data hierarchy, e.g.:

```
/workspaces/<workspace_pk>/projects/<project_pk>/tasks/<pk>/
/workspaces/<workspace_pk>/projects/<project_pk>/tasks/<task_pk>/comments/<pk>/edit/
```

## Features

- Auth: register, login, logout, edit profile, profile picture upload
- Full CRUD on Workspace, Project, Task, Comment
- Task assignment restricted to workspace members
- Dashboard: workspace/project/task counts, tasks-by-status breakdown, tasks
  assigned to me, recent tasks
- Search (project name, task title) + filters (task status, task priority)
- Pagination on Project and Task lists, filters preserved across pages
- Django Messages framework for user feedback on every create/update/delete
- Function-based views throughout, `ModelForm`s, `login_required`,
  `related_name` on every FK, `Meta.ordering` on every model

## Running Locally

```bash
python -m venv venv
source venv/bin/activate        # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env            # then edit .env with your own SECRET_KEY
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Running Tests

```bash
python manage.py test
```

Covers model behavior (e.g. `on_delete=SET_NULL` for task assignment),
permission boundaries (non-members get 403, non-owners can't
edit/delete, only a comment's author can edit/delete it), and
task search/filtering.

## Talking Points for Interviews

- Why nested URLs instead of flat ones with query params: it mirrors the
  actual data hierarchy and makes `get_object_or_404` double as an
  authorization check — a task can only ever be found through the workspace
  and project it actually belongs to.
- Why `assigned_to` uses `on_delete=SET_NULL`: deleting a user shouldn't
  cascade-delete every task they were ever assigned; the task should just
  become unassigned.
- Why permissions are function-level checks instead of a permissions
  framework: at this scale (single owner + members, no per-object roles) a
  framework would add indirection without adding real flexibility.
