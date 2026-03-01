from django.db.models import QuerySet
from .models import Project
from apps.accounts.models import User

def list_user_projects(user: User) -> QuerySet[Project]:
    return Project.objects.filter(owner=user)

def get_project_for_user(project_id: str, user: User) -> Project | None:
    return Project.objects.filter(id=project_id, owner=user).first()
