from django.contrib import admin

# Register your models here.
from .models import Question, TodoItem

admin.site.register(Question)
admin.site.register(TodoItem)