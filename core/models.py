from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class UserEmail(models.Model):
    email = models.EmailField(_('Email'), unique=True)
    source = models.CharField(_('Izvor'), max_length=50, choices=[
        ('contact', _('Kontakt forma')),
        ('registration', _('Registracija')),
    ])
    created_at = models.DateTimeField(_('Kreirano'), auto_now_add=True)

    class Meta:
        verbose_name = _('Email korisnika')
        verbose_name_plural = _('Emailovi korisnika')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.email} ({self.get_source_display()})"


class CkeditorUpload(models.Model):
    """
    Track CKEditor uploads to detect orphaned files.
    When a file is uploaded to CKEditor, it's tracked here.
    When a product/blog is saved, we check if tracked uploads are used.
    If not used, they're deleted from R2.
    """
    file_path = models.CharField(_('Putanja fajla'), max_length=500, unique=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    uploaded_at = models.DateTimeField(_('Uploadovano'), auto_now_add=True)
    is_used = models.BooleanField(_('Korišćeno'), default=False)
    used_in_model = models.CharField(_('Korišćeno u'), max_length=100, blank=True)  # 'Product' or 'BlogPost'
    used_in_id = models.IntegerField(_('ID instance'), null=True, blank=True)
    
    class Meta:
        verbose_name = _('CKEditor upload')
        verbose_name_plural = _('CKEditor uploadi')
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['is_used', 'uploaded_at']),
        ]

    def __str__(self):
        return f"{self.file_path} ({'Used' if self.is_used else 'Unused'})"
