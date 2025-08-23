from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Instructor


class CustomInstructorAdmin(admin.ModelAdmin):

    list_display = ['user__first_name', 'user__last_name', 'user__email',  'user__is_staff']
    ordering = ("user__last_name",)

    # If you want to customize what fields show when adding a new User:
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('status'),
        }),
    )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []  # don’t show profile inline when creating a new user
        return super().get_inline_instances(request, obj)
    


admin.site.register(Instructor, CustomInstructorAdmin)
