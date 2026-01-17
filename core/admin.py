from django.contrib import admin
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
import csv
from .models import UserEmail, CkeditorUpload


@admin.register(UserEmail)
class UserEmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'source', 'created_at')
    list_filter = ('source', 'created_at')
    search_fields = ('email',)
    actions = ['export_as_csv', 'export_all_as_csv']
    date_hierarchy = 'created_at'

    def export_as_csv(self, request, queryset):
        """Export selected emails to CSV"""
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="emails_selected.csv"'
        writer = csv.writer(response)
        writer.writerow([_('Email'), _('Izvor'), _('Kreirano')])
        for email in queryset:
            writer.writerow([email.email, email.get_source_display(), email.created_at.strftime('%Y-%m-%d %H:%M:%S')])
        return response
    export_as_csv.short_description = _('Izvezi izabrane emailove u CSV')
    
    def export_all_as_csv(self, request, queryset):
        """Export all emails to CSV"""
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="emails_all.csv"'
        writer = csv.writer(response)
        writer.writerow([_('Email'), _('Izvor'), _('Kreirano')])
        for email in UserEmail.objects.all().order_by('-created_at'):
            writer.writerow([email.email, email.get_source_display(), email.created_at.strftime('%Y-%m-%d %H:%M:%S')])
        return response
    export_all_as_csv.short_description = _('Izvezi sve emailove u CSV')


@admin.register(CkeditorUpload)
class CkeditorUploadAdmin(admin.ModelAdmin):
    list_display = ('file_path', 'uploaded_by', 'is_used', 'used_in_model', 'uploaded_at')
    list_filter = ('is_used', 'used_in_model', 'uploaded_at')
    search_fields = ('file_path',)
    readonly_fields = ('uploaded_at',)
    date_hierarchy = 'uploaded_at'
