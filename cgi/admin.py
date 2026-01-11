from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

admin.site.site_header = _('CGI administracija')
admin.site.site_title = _('CGI administracija')
admin.site.index_title = _('CGI administracija')

# Unregister Group model
admin.site.unregister(Group)


