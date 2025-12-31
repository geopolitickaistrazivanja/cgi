from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django import forms
from django.core.exceptions import ValidationError
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Product, ProductImage, ProductDimension, ProductPattern


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'order')
    can_delete = True


class ProductDimensionInline(admin.TabularInline):
    model = ProductDimension
    extra = 1
    fields = ('length', 'width', 'height', 'price', 'order')
    can_delete = True


class ProductPatternInline(admin.TabularInline):
    model = ProductPattern
    extra = 1
    fields = ('image', 'order')
    can_delete = True


@admin.register(ProductDimension)
class ProductDimensionAdmin(admin.ModelAdmin):
    list_display = ('product', 'length', 'width', 'height', 'order')
    list_filter = ('product',)
    search_fields = ('product__title',)


@admin.register(ProductPattern)
class ProductPatternAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'order')
    list_filter = ('product',)
    search_fields = ('product__title',)


class ProductAdminForm(forms.ModelForm):
    """Custom form with better validation and error messages"""
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'short_description': CKEditorUploadingWidget(config_name='default'),
            'full_description': CKEditorUploadingWidget(config_name='default'),
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title or not title.strip():
            raise ValidationError(_('Naslov proizvoda je obavezan.'))
        return title
    
    def clean_sku(self):
        sku = self.cleaned_data.get('sku')
        if not sku or not sku.strip():
            raise ValidationError(_('SKU je obavezan.'))
        return sku
    
    def clean_meta_title(self):
        meta_title = self.cleaned_data.get('meta_title')
        if not meta_title or not meta_title.strip():
            raise ValidationError(_('Meta naslov je obavezan za SEO.'))
        return meta_title
    
    def clean_meta_description(self):
        meta_description = self.cleaned_data.get('meta_description')
        if not meta_description or not meta_description.strip():
            raise ValidationError(_('Meta opis je obavezan za SEO.'))
        return meta_description
    
    def clean_stock_quantity(self):
        stock_quantity = self.cleaned_data.get('stock_quantity')
        stock_type = self.cleaned_data.get('stock_type')
        
        if stock_type == 'limited':
            if not stock_quantity or stock_quantity <= 0:
                raise ValidationError(_('Količina na stanju mora biti veća od 0 kada je tip zaliha "Ograničena količina".'))
        return stock_quantity


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('title', 'sku', 'stock_status', 'is_active', 'created_at')
    list_filter = ('stock_type', 'is_active', 'created_at')
    search_fields = ('title', 'sku', 'short_description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductImageInline, ProductDimensionInline, ProductPatternInline]
    fieldsets = (
        (_('Osnovne informacije'), {
            'fields': ('title', 'slug', 'sku')
        }),
        (_('SEO'), {
            'fields': ('meta_title', 'meta_description')
        }),
        (_('Slika'), {
            'fields': ('thumbnail',)
        }),
        (_('Opis'), {
            'fields': ('short_description', 'full_description')
        }),
        (_('Zalihe'), {
            'fields': ('stock_type', 'stock_quantity', 'is_active')
        }),
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name in ('short_description', 'full_description'):
            kwargs['widget'] = CKEditorUploadingWidget(config_name='default')
        return super().formfield_for_dbfield(db_field, request, **kwargs)
    
    class Media:
        js = ('admin/js/product_admin.js',)

    def stock_status(self, obj):
        if obj.stock_type == 'always':
            return _('Uvek na stanju')
        if obj.stock_quantity and obj.stock_quantity > 0:
            return f"{obj.stock_quantity} komada"
        return _('Nema na stanju')
    stock_status.short_description = _('Status zaliha')
