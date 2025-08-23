from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .models import UserProfile


User = get_user_model()

class ProfileInline(admin.StackedInline):
        model = UserProfile
        can_delete = False  # Prevents deletion of the Profile when deleting the User
        verbose_name_plural = 'profile'
        fk_name = 'user' # Specifies the foreign key field in Profile that links to User

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

    list_display = ['first_name', 'last_name', 'email', 'get_role', 'is_staff']
    ordering = ("last_name",)

    # If you want to customize what fields show when adding a new User:
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []  # don’t show profile inline when creating a new user
        return super().get_inline_instances(request, obj)
    
    def get_role(self, obj):
        return obj.profile.role if hasattr(obj, 'profile') else "-"
    get_role.short_description = 'Role'


admin.site.register(User, CustomUserAdmin)
