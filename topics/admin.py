from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Topic, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'slug', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('order',)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    fieldsets = (
        (_('Osnovne informacije'), {
            'fields': ('name', 'slug', 'thumbnail', 'order')
        }),
    )


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'slug', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'short_description', 'full_description')
    prepopulated_fields = {'slug': ('title',)}
    
    class Meta:
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'
    fieldsets = (
        (_('Osnovne informacije'), {
            'fields': ('title', 'slug', 'category', 'thumbnail')
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
