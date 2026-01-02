from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'short_description', 'full_description')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (_('Osnovne informacije'), {
            'fields': ('title', 'slug', 'thumbnail')
        }),
        (_('SEO'), {
            'fields': ('meta_title', 'meta_description')
        }),
        (_('Opis'), {
            'fields': ('short_description', 'full_description')
        }),
    )
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name in ('short_description', 'full_description'):
            kwargs['widget'] = CKEditorUploadingWidget(config_name='default')
        return super().formfield_for_dbfield(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        """
        Override save_model to pass request to cleanup function.
        This allows us to access session uploads for cleanup.
        """
        # Store request in obj temporarily so cleanup can access it
        obj._request = request
        super().save_model(request, obj, form, change)
        # Clean up after save
        if hasattr(obj, '_request'):
            delattr(obj, '_request')
