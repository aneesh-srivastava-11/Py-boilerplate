from django.db import transaction
from .models import Project
from apps.accounts.models import User

@transaction.atomic
def create_project(*, name: str, description: str, owner: User) -> Project:
    project = Project(name=name, description=description, owner=owner)
    project.full_clean()
    project.save()
    return project

@transaction.atomic
def update_project(project: Project, **data) -> Project:
    for field, value in data.items():
        setattr(project, field, value)
    project.full_clean()
    project.save()
    return project
