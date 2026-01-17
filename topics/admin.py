from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Topic, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'slug', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'name_sr_cyrl', 'name_en')
    prepopulated_fields = {
        'slug': ('name',),
        'slug_sr_cyrl': ('name_sr_cyrl',),
        'slug_en': ('name_en',),
    }
    list_editable = ('order',)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    fieldsets = (
        (_('Srpski (latinica)'), {
            'fields': ('name', 'slug')
        }),
        (_('Српски (ћирилица)'), {
            'fields': ('name_sr_cyrl', 'slug_sr_cyrl')
        }),
        (_('English'), {
            'fields': ('name_en', 'slug_en')
        }),
        (_('Ostalo'), {
            'fields': ('thumbnail', 'order')
        }),
    )


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'slug', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'title_sr_cyrl', 'title_en', 'short_description', 'full_description')
    prepopulated_fields = {
        'slug': ('title',),
        'slug_sr_cyrl': ('title_sr_cyrl',),
        'slug_en': ('title_en',),
    }
    
    class Meta:
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'
    fieldsets = (
        (_('Srpski (latinica)'), {
            'fields': ('title', 'slug', 'meta_title', 'meta_description', 'short_description', 'full_description')
        }),
        (_('Српски (ћирилица)'), {
            'fields': ('title_sr_cyrl', 'slug_sr_cyrl', 'meta_title_sr_cyrl', 'meta_description_sr_cyrl', 'short_description_sr_cyrl', 'full_description_sr_cyrl')
        }),
        (_('English'), {
            'fields': ('title_en', 'slug_en', 'meta_title_en', 'meta_description_en', 'short_description_en', 'full_description_en')
        }),
        (_('Ostalo'), {
            'fields': ('category', 'thumbnail')
        }),
    )
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name in ('short_description', 'full_description', 
                             'short_description_sr_cyrl', 'full_description_sr_cyrl',
                             'short_description_en', 'full_description_en'):
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
