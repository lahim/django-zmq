from django.contrib import admin

from djangozmq import models


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'status', 'execution_time')
    search_fields = ('uuid', 'name', 'status')
