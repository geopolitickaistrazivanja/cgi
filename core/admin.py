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
    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="emails.csv"'
        writer = csv.writer(response)
        writer.writerow(['Email', 'Izvor', 'Kreirano'])
        for email in queryset:
            writer.writerow([email.email, email.get_source_display(), email.created_at.strftime('%Y-%m-%d %H:%M:%S')])
        return response
    export_as_csv.short_description = _('Izvezi izabrane emailove u CSV')


@admin.register(CkeditorUpload)
class CkeditorUploadAdmin(admin.ModelAdmin):
    list_display = ('file_path', 'uploaded_by', 'is_used', 'used_in_model', 'uploaded_at')
    list_filter = ('is_used', 'used_in_model', 'uploaded_at')
    search_fields = ('file_path',)
    readonly_fields = ('uploaded_at',)
    date_hierarchy = 'uploaded_at'
