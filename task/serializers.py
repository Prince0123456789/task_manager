# tasks/serializers.py
from rest_framework import serializers
from user.models import User
from task.models import Task


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'completed', 'created_at', 'updated_at', 'owner')
        read_only_fields = ('id', 'created_at', 'updated_at', 'owner')
