from django.contrib import admin
from task.models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id','title','created_at','updated_at']
    model = Task