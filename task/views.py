from django.shortcuts import render

from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Task
from .serializers import TaskSerializer
from user.permissions import IsOwnerOrAdmin
from .filters import TaskFilter
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related('owner').all()
    serializer_class = TaskSerializer
    permission_classes = [IsOwnerOrAdmin]
    filterset_class = TaskFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at']
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        # Allow anyone to list/retrieve; require auth for create/update/delete
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]
