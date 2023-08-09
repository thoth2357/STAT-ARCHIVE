from typing import Any, Dict, List, Optional, Tuple
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http.request import HttpRequest
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    
    list_display = [
        'username',
        'email',
        'fullname',
        'is_email_verified',
        'is_approved',
        'date_joined',
    ]
    
    def get_fieldsets(self, request: HttpRequest, obj: Any | None = ...) -> List[Tuple[str | None, Dict[str, Any]]]:
        if request.user.is_superuser:
            fieldsets = (
                (None, {'fields': ('username', 'password')}),
                ('Personal info', {'fields': ('email', 'fullname', 'is_email_verified', 'is_approved')}),
                ('Reset Password', {'fields': ('reset_token', 'reset_token_expiration')}),
                ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
                ('Important dates', {'fields': ('last_login', 'date_joined')}),
            )
        else:
            # Fieldsets for staff user
            fieldsets = (
                (None, {'fields': ('username', )}),
                ('Personal info', {'fields': ('email', 'fullname', 'is_approved')}),
                ('Important dates', {'fields': ('last_login', 'date_joined')}),
            )
        return fieldsets
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        
        # Check if the logged-in user is in the "Staff" group
        if request.user.groups.filter(name='Classrep').exists():
            # Extract the first five characters from staff user's username
            classrep_username_prefix = request.user.username[:5]
            
            # Filter queryset to show only users with matching matric number prefix
            queryset = queryset.filter(username__startswith=classrep_username_prefix)

        return queryset

    # Define readonly fields for Classrep users
    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name='Classrep').exists():
            return [field.name for field in self.model._meta.fields if field.name != 'is_approved']
        return self.readonly_fields

admin.site.site_header = "STA Archive Admin Dashboard"

admin.site.register(User, CustomUserAdmin)
