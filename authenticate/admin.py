from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from blog.models import Blog
from authenticate.models import User
# Register your models here.

class BlogAdmin(admin.TabularInline):
    model = Blog

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (
            None,
            {
                'fields': ('email', 'password','username', 'first_name', 'last_name', 'last_login')
            }
        ),
        (
            'Permissions',
            {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups','user_permissions',)
            }
        ),
    )
    inlines = [
        BlogAdmin,
    ]
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'username', 'password1', 'password2')
            }
        ),
    )

    list_display = ('email', 'username', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(User, UserAdmin)