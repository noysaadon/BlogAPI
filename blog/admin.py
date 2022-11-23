from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from blog.models import Blog, Like
# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    model = Blog
    list_display = ['title', 'description']

admin.site.register(Blog, BlogAdmin)
admin.site.register(Like)