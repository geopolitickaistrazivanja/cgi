from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import PermissionDenied
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = _('Profil')


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of superusers in admin UI"""
        if obj is not None and obj.is_superuser:
            return False
        return super().has_delete_permission(request, obj)
    
    def delete_queryset(self, request, queryset):
        """Prevent bulk deletion of superusers"""
        superusers = queryset.filter(is_superuser=True)
        if superusers.exists():
            from django.contrib import messages
            messages.error(request, _('Ne možete obrisati superkorisnike.'))
            queryset = queryset.exclude(is_superuser=True)
        super().delete_queryset(request, queryset)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (_('Korisnik'), {
            'fields': ('user',)
        }),
        (_('Kontakt informacije'), {
            'fields': ('phone', 'address')
        }),
        (_('Datumi'), {
            'fields': ('created_at', 'updated_at')
        }),
    )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
