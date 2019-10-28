from django.contrib import admin

from task.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ['task', 'status', 'start_time', 'end_time']


admin.site.register(Task, TaskAdmin)
