from django.test import TestCase
from apps.accounts.models import User
from .services import create_project
from .models import Project

class ProjectServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='password123')

    def test_create_project(self):
        project = create_project(
            name="Test Project",
            description="Testing services",
            owner=self.user
        )
        self.assertEqual(project.name, "Test Project")
        self.assertEqual(project.owner, self.user)
        self.assertTrue(Project.objects.filter(id=project.id).exists())
