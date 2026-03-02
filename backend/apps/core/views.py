from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.common.responses import success_response
from apps.common.pagination import StandardResultsSetPagination
from .serializers import ProjectSerializer
from .services import create_project, update_project
from .selectors import list_user_projects, get_project_for_user

class ProjectListCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        projects = list_user_projects(request.user)
        
        paginator = StandardResultsSetPagination()
        paginated_projects = paginator.paginate_queryset(projects, request, view=self)
        
        serializer = ProjectSerializer(paginated_projects, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        project = create_project(
            owner=request.user,
            **serializer.validated_data
        )
        data = ProjectSerializer(project).data
        return success_response(data, "Project created successfully", status.HTTP_201_CREATED)

class ProjectDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        project = get_object_or_404(list_user_projects(request.user), pk=pk)
        serializer = ProjectSerializer(project)
        return success_response(serializer.data, "Project fetched successfully")

    def patch(self, request, pk):
        project = get_object_or_404(list_user_projects(request.user), pk=pk)
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        project = update_project(project, **serializer.validated_data)
        return success_response(ProjectSerializer(project).data, "Project updated successfully")

    def delete(self, request, pk):
        project = get_object_or_404(list_user_projects(request.user), pk=pk)
        project.delete() # Or soft delete via services.py
        return success_response(message="Project deleted successfully", status_code=status.HTTP_204_NO_CONTENT)
