from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import UserProfile, Order, OrderItem


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = _('Profil')


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product', 'quantity', 'price', 'get_dimension_display', 'get_pattern_display', 'get_subtotal')
    readonly_fields = ('get_subtotal', 'get_dimension_display', 'get_pattern_display')
    can_delete = True

    def get_subtotal(self, obj):
        if obj and obj.pk and obj.quantity and obj.price:
            return f"{obj.subtotal:.2f} RSD"
        return "-"
    get_subtotal.short_description = _('Ukupno')
    
    def get_dimension_display(self, obj):
        if obj and obj.selected_dimension:
            return obj.selected_dimension.get_display()
        return "-"
    get_dimension_display.short_description = _('Dimenzije')
    
    def get_pattern_display(self, obj):
        if obj and obj.selected_pattern:
            from django.utils.html import format_html
            return format_html('<img src="{}" style="max-width: 100px; border: 1px solid #ddd; border-radius: 4px;">', obj.selected_pattern.image.url)
        return "-"
    get_pattern_display.short_description = _('Dezen')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'email', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderItemInline]
    fieldsets = (
        (_('Korisnik'), {
            'fields': ('user', 'email')
        }),
        (_('Podaci za dostavu'), {
            'fields': ('first_name', 'last_name', 'phone', 'address', 'city', 'postal_code')
        }),
        (_('Status'), {
            'fields': ('status', 'total_amount')
        }),
        (_('Datumi'), {
            'fields': ('created_at', 'updated_at')
        }),
    )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
