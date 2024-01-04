from django.contrib import admin

from django.contrib import admin
from .models import ToDoList


@admin.register(ToDoList)
class ToDoList(admin.ModelAdmin):
    list_display = ('title', 'details', 'date', 'progress', 'deleted', 'created_by')


